from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
import shutil
import json

ROOT_DIR = Path(__file__).parent

# Load environment variables based on environment
# In production (Render), use system environment variables
# In development, load from .env file
if os.environ.get('RENDER'):
    # Production: Render sets this environment variable automatically
    # Use system environment variables (configured in Render dashboard)
    pass
else:
    # Development: Load from local .env file
    load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
SECRET_KEY = os.environ.get('JWT_SECRET', 'karaoke_secret_key_change_in_production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

security = HTTPBearer()

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Models
class Singer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    email: Optional[str] = None
    codice: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Song(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    singer_id: str
    canzone: str
    tonalita: str
    ordine_prenotazione: int
    cantata: bool = False
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore")
    prenotazioni_aperte: bool = True

class BookingRequest(BaseModel):
    nome: str
    email: Optional[str] = None
    canzone: str
    tonalita: str
    codice: Optional[str] = None

class BookingResponse(BaseModel):
    success: bool
    codice: str
    message: str
    nuovo_cantante: bool

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SingerWithSongs(BaseModel):
    id: str
    nome: str
    codice: str
    canzoni: List[Song]
    timestamp: str

class Stats(BaseModel):
    totale_prenotazioni: int
    canzoni_cantate: int
    in_attesa: int
    totale_cantanti: int

class UpdateSongRequest(BaseModel):
    cantata: Optional[bool] = None
    ordine_prenotazione: Optional[int] = None

class License(BaseModel):
    model_config = ConfigDict(extra="ignore")
    license_key: str
    email: str
    plan: str  # daily, monthly, yearly
    status: str = "active"  # active, expired, suspended
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str
    hwid: Optional[str] = None
    last_check: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LicenseCreate(BaseModel):
    email: str
    plan: str  # daily, monthly, yearly

class LicenseVerify(BaseModel):
    license_key: str
    hwid: Optional[str] = None

class AdminCredentials(BaseModel):
    username: str
    password: str

class AdminUpdate(BaseModel):
    current_password: str
    new_username: Optional[str] = None
    new_password: Optional[str] = None

class AdminCreate(BaseModel):
    username: str
    password: str
    role: str = "admin"  # default: admin, può essere "super_admin"

class LicenseInfo(BaseModel):
    has_license: bool
    license_key: Optional[str] = None
    plan: Optional[str] = None
    expires_at: Optional[str] = None
    days_remaining: Optional[int] = None
    status: Optional[str] = None
    unlimited: bool = False
    role: str = "admin"

class Serata(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nome: str
    data: str
    folder_path: str
    display_time: int = 5  # secondi per mostrare ogni foto
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    active: bool = True

class SerataCreate(BaseModel):
    nome: str
    display_time: int = 5

class EmailConfig(BaseModel):
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str
    sender_password: str

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def verify_token_and_license(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica token JWT e validità licenza"""
    username = await verify_token(credentials)
    
    # Recupera admin
    admin = await db.admins.find_one({"username": username})
    if not admin:
        raise HTTPException(status_code=401, detail="Admin non trovato")
    
    # Super admin ha sempre accesso
    if admin.get("role") == "super_admin":
        return username
    
    # Verifica licenza
    license_key = admin.get("license_key")
    if not license_key:
        raise HTTPException(status_code=403, detail="Nessuna licenza associata")
    
    license_doc = await db.licenses.find_one({"license_key": license_key})
    if not license_doc:
        raise HTTPException(status_code=403, detail="Licenza non trovata")
    
    # Controlla scadenza
    expires_at = datetime.fromisoformat(license_doc['expires_at'])
    now = datetime.now(timezone.utc)
    
    if now > expires_at:
        # Aggiorna stato a expired
        await db.licenses.update_one(
            {"license_key": license_key},
            {"$set": {"status": "expired"}}
        )
        raise HTTPException(status_code=403, detail="Licenza scaduta")
    
    if license_doc.get('status') != "active":
        raise HTTPException(status_code=403, detail=f"Licenza {license_doc['status']}")
    
    return username

async def get_next_codice():
    # Get highest code number
    singers = await db.singers.find({}).to_list(None)
    if not singers:
        return "001"
    codes = [int(s['codice']) for s in singers if s['codice'].isdigit()]
    if not codes:
        return "001"
    return str(max(codes) + 1).zfill(3)

async def get_next_order():
    songs = await db.songs.find({}).to_list(None)
    if not songs:
        return 1
    orders = [s['ordine_prenotazione'] for s in songs]
    return max(orders) + 1 if orders else 1

def generate_license_key():
    """Genera un codice licenza unico formato: KAR-XXXX-XXXX-XXXX"""
    import random
    import string
    parts = []
    for _ in range(3):
        part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        parts.append(part)
    return f"KAR-{'-'.join(parts)}"

def calculate_expiry_date(plan: str):
    """Calcola la data di scadenza in base al piano"""
    now = datetime.now(timezone.utc)
    if plan == "daily":
        return (now + timedelta(days=1)).isoformat()
    elif plan == "monthly":
        return (now + timedelta(days=30)).isoformat()
    elif plan == "yearly":
        return (now + timedelta(days=365)).isoformat()
    return now.isoformat()

# Initialize admin user and settings
@app.on_event("startup")
async def startup_event():
    # Create default admin if not exists
    admin = await db.admins.find_one({"username": "admin"})
    if not admin:
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        await db.admins.insert_one({
            "username": "admin",
            "password": hashed_password.decode('utf-8'),
            "role": "admin",
            "license_key": None  # Verrà associato dopo
        })
    
    # Create super admin if not exists (TUO account con accesso illimitato)
    super_admin = await db.admins.find_one({"role": "super_admin"})
    if not super_admin:
        hashed_password = bcrypt.hashpw("superadmin123".encode('utf-8'), bcrypt.gensalt())
        await db.admins.insert_one({
            "username": "superadmin",
            "password": hashed_password.decode('utf-8'),
            "role": "super_admin",
            "unlimited": True
        })
    
    # Create default settings if not exists
    settings = await db.settings.find_one({})
    if not settings:
        await db.settings.insert_one({"prenotazioni_aperte": True})

# Public Routes
@api_router.get("/")
async def root():
    return {"message": "Karaoke Booking System"}

@api_router.get("/settings")
async def get_settings():
    settings = await db.settings.find_one({}, {"_id": 0})
    if not settings:
        return {"prenotazioni_aperte": True}
    return settings

@api_router.post("/book", response_model=BookingResponse)
async def create_booking(booking: BookingRequest):
    # Check if bookings are open
    settings = await db.settings.find_one({})
    if settings and not settings.get('prenotazioni_aperte', True):
        raise HTTPException(status_code=400, detail="Le prenotazioni sono finite")
    
    nuovo_cantante = False
    
    # If codice provided, verify it
    if booking.codice:
        singer = await db.singers.find_one({"codice": booking.codice})
        if not singer:
            raise HTTPException(status_code=400, detail="Codice non trovato")
        if singer['nome'].lower() != booking.nome.lower():
            raise HTTPException(status_code=400, detail="Il nome non corrisponde al codice inserito")
        singer_id = singer['id']
        codice = booking.codice
        # Aggiorna email se fornita e non già presente
        if booking.email and not singer.get('email'):
            await db.singers.update_one({"id": singer_id}, {"$set": {"email": booking.email}})
    else:
        # Create new singer
        codice = await get_next_codice()
        singer = Singer(nome=booking.nome, email=booking.email, codice=codice)
        await db.singers.insert_one(singer.model_dump())
        singer_id = singer.id
        nuovo_cantante = True
    
    # Create song booking
    ordine = await get_next_order()
    song = Song(
        singer_id=singer_id,
        canzone=booking.canzone,
        tonalita=booking.tonalita,
        ordine_prenotazione=ordine
    )
    await db.songs.insert_one(song.model_dump())
    
    message = f"Prenotazione confermata! Il tuo codice è {codice}. Ricordalo per le prossime prenotazioni." if nuovo_cantante else "Prenotazione aggiunta!"
    
    return BookingResponse(
        success=True,
        codice=codice,
        message=message,
        nuovo_cantante=nuovo_cantante
    )

# Admin Routes
@api_router.post("/admin/login", response_model=LoginResponse)
async def admin_login(login: LoginRequest):
    admin = await db.admins.find_one({"username": login.username})
    if not admin:
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    
    # admin['password'] is already bytes from MongoDB, no need to encode
    if not bcrypt.checkpw(login.password.encode('utf-8'), admin['password']):
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    
    access_token = create_access_token(data={"sub": login.username})
    return LoginResponse(access_token=access_token)

@api_router.get("/admin/singers", response_model=List[SingerWithSongs])
async def get_singers(username: str = Depends(verify_token_and_license)):
    singers = await db.singers.find({}, {"_id": 0}).to_list(None)
    result = []
    
    for singer in singers:
        songs = await db.songs.find({"singer_id": singer['id']}, {"_id": 0}).to_list(None)
        songs_sorted = sorted(songs, key=lambda x: x['ordine_prenotazione'])
        result.append(SingerWithSongs(
            id=singer['id'],
            nome=singer['nome'],
            codice=singer['codice'],
            canzoni=[Song(**song) for song in songs_sorted],
            timestamp=singer['timestamp']
        ))
    
    # Sort by timestamp (first to arrive first)
    result.sort(key=lambda x: x.timestamp)
    return result

@api_router.get("/admin/stats", response_model=Stats)
async def get_stats(username: str = Depends(verify_token_and_license)):
    songs = await db.songs.find({}, {"_id": 0}).to_list(None)
    singers = await db.singers.find({}, {"_id": 0}).to_list(None)
    
    totale_prenotazioni = len(songs)
    canzoni_cantate = sum(1 for song in songs if song.get('cantata', False))
    in_attesa = totale_prenotazioni - canzoni_cantate
    totale_cantanti = len(singers)
    
    return Stats(
        totale_prenotazioni=totale_prenotazioni,
        canzoni_cantate=canzoni_cantate,
        in_attesa=in_attesa,
        totale_cantanti=totale_cantanti
    )

@api_router.put("/admin/song/{song_id}")
async def update_song(song_id: str, update: UpdateSongRequest, username: str = Depends(verify_token_and_license)):
    song = await db.songs.find_one({"id": song_id})
    if not song:
        raise HTTPException(status_code=404, detail="Canzone non trovata")
    
    update_data = {}
    if update.cantata is not None:
        update_data['cantata'] = update.cantata
    if update.ordine_prenotazione is not None:
        update_data['ordine_prenotazione'] = update.ordine_prenotazione
    
    await db.songs.update_one({"id": song_id}, {"$set": update_data})
    return {"success": True}

@api_router.delete("/admin/song/{song_id}")
async def delete_song(song_id: str, username: str = Depends(verify_token)):
    result = await db.songs.delete_one({"id": song_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Canzone non trovata")
    return {"success": True}

@api_router.delete("/admin/singer/{singer_id}")
async def delete_singer(singer_id: str, username: str = Depends(verify_token)):
    # Delete all songs for this singer
    await db.songs.delete_many({"singer_id": singer_id})
    # Delete singer
    result = await db.singers.delete_one({"id": singer_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cantante non trovato")
    return {"success": True}

@api_router.put("/admin/settings")
async def update_settings(settings: Settings, username: str = Depends(verify_token)):
    await db.settings.update_one({}, {"$set": settings.model_dump()}, upsert=True)
    return {"success": True}

@api_router.delete("/admin/reset-all")
async def reset_all(username: str = Depends(verify_token)):
    """Reset completo: cancella tutti i cantanti e tutte le canzoni"""
    await db.singers.delete_many({})
    await db.songs.delete_many({})
    return {"success": True, "message": "Serata resettata completamente"}

@api_router.delete("/admin/clear-sung")
async def clear_sung_songs(username: str = Depends(verify_token)):
    """Elimina solo le canzoni già cantate, mantiene i cantanti"""
    result = await db.songs.delete_many({"cantata": True})
    return {"success": True, "deleted_count": result.deleted_count, "message": f"{result.deleted_count} canzoni cantate eliminate"}

# ============================================
# LICENSING SYSTEM ENDPOINTS
# ============================================

@api_router.post("/license/verify")
async def verify_license(verify_data: LicenseVerify):
    """Verifica se una licenza è valida"""
    license_doc = await db.licenses.find_one({"license_key": verify_data.license_key})
    
    if not license_doc:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    # Controlla se la licenza è scaduta
    expires_at = datetime.fromisoformat(license_doc['expires_at'])
    now = datetime.now(timezone.utc)
    
    if now > expires_at and license_doc['status'] == "active":
        # Aggiorna stato a expired
        await db.licenses.update_one(
            {"license_key": verify_data.license_key},
            {"$set": {"status": "expired"}}
        )
        raise HTTPException(status_code=403, detail="Licenza scaduta")
    
    if license_doc['status'] != "active":
        raise HTTPException(status_code=403, detail=f"Licenza {license_doc['status']}")
    
    # Aggiorna last_check e hwid
    update_data = {"last_check": datetime.now(timezone.utc).isoformat()}
    if verify_data.hwid:
        update_data["hwid"] = verify_data.hwid
    
    await db.licenses.update_one(
        {"license_key": verify_data.license_key},
        {"$set": update_data}
    )
    
    return {
        "valid": True,
        "plan": license_doc['plan'],
        "expires_at": license_doc['expires_at'],
        "status": "active"
    }

# ============================================
# SUPER ADMIN ENDPOINTS (gestione licenze)
# ============================================

async def verify_super_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica che l'utente sia super admin"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Verifica che sia super admin
        admin = await db.admins.find_one({"username": username})
        if not admin or admin.get("role") != "super_admin":
            raise HTTPException(status_code=403, detail="Super admin access required")
        
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@api_router.post("/super-admin/license/create")
async def create_license(license_create: LicenseCreate, username: str = Depends(verify_super_admin)):
    """Crea una nuova licenza (solo super admin)"""
    license_key = generate_license_key()
    expires_at = calculate_expiry_date(license_create.plan)
    
    license_doc = License(
        license_key=license_key,
        email=license_create.email,
        plan=license_create.plan,
        expires_at=expires_at
    )
    
    await db.licenses.insert_one(license_doc.model_dump())
    
    return {
        "success": True,
        "license_key": license_key,
        "expires_at": expires_at,
        "plan": license_create.plan
    }

@api_router.get("/super-admin/licenses")
async def get_all_licenses(username: str = Depends(verify_super_admin)):
    """Ottieni tutte le licenze (solo super admin)"""
    licenses = await db.licenses.find({}, {"_id": 0}).to_list(None)
    
    # Aggiungi informazioni su scadenza
    for lic in licenses:
        expires_at = datetime.fromisoformat(lic['expires_at'])
        now = datetime.now(timezone.utc)
        lic['days_remaining'] = (expires_at - now).days
        lic['is_expired'] = now > expires_at
    
    return licenses

@api_router.put("/super-admin/license/{license_key}/status")
async def update_license_status(license_key: str, status: str, username: str = Depends(verify_super_admin)):
    """Cambia lo stato di una licenza: active, suspended, expired"""
    if status not in ["active", "suspended", "expired"]:
        raise HTTPException(status_code=400, detail="Status non valido")
    
    result = await db.licenses.update_one(
        {"license_key": license_key},
        {"$set": {"status": status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    return {"success": True, "license_key": license_key, "new_status": status}

@api_router.delete("/super-admin/license/{license_key}")
async def delete_license(license_key: str, username: str = Depends(verify_super_admin)):
    """Elimina una licenza (solo super admin)"""
    result = await db.licenses.delete_one({"license_key": license_key})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    return {"success": True, "message": "Licenza eliminata"}

@api_router.put("/super-admin/license/{license_key}/extend")
async def extend_license(license_key: str, days: int, username: str = Depends(verify_super_admin)):
    """Estende una licenza di X giorni (solo super admin)"""
    license_doc = await db.licenses.find_one({"license_key": license_key})
    
    if not license_doc:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    current_expiry = datetime.fromisoformat(license_doc['expires_at'])
    new_expiry = current_expiry + timedelta(days=days)
    
    await db.licenses.update_one(
        {"license_key": license_key},
        {"$set": {"expires_at": new_expiry.isoformat(), "status": "active"}}
    )
    
    return {
        "success": True,
        "license_key": license_key,
        "new_expires_at": new_expiry.isoformat(),
        "days_added": days
    }

# ============================================
# ADMIN CREDENTIALS MANAGEMENT
# ============================================

@api_router.put("/admin/credentials")
async def update_admin_credentials(update: AdminUpdate, username: str = Depends(verify_token)):
    """Permette all'admin di cambiare username e/o password"""
    admin = await db.admins.find_one({"username": username})
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trovato")
    
    # Verifica password corrente
    # admin['password'] is already bytes from MongoDB
    if not bcrypt.checkpw(update.current_password.encode('utf-8'), admin['password']):
        raise HTTPException(status_code=401, detail="Password corrente non valida")
    
    update_data = {}
    
    # Aggiorna username se fornito
    if update.new_username:
        # Verifica che il nuovo username non sia già in uso
        existing = await db.admins.find_one({"username": update.new_username})
        if existing and existing['username'] != username:
            raise HTTPException(status_code=400, detail="Username già in uso")
        update_data['username'] = update.new_username
    
    # Aggiorna password se fornita
    if update.new_password:
        hashed_password = bcrypt.hashpw(update.new_password.encode('utf-8'), bcrypt.gensalt())
        # Store as bytes in MongoDB, like in startup event
        update_data['password'] = hashed_password
    
    if update_data:
        await db.admins.update_one({"username": username}, {"$set": update_data})
        
        # Genera nuovo token se username è cambiato
        new_username = update_data.get('username', username)
        new_token = create_access_token(data={"sub": new_username})
        
        return {
            "success": True,
            "message": "Credenziali aggiornate",
            "new_token": new_token if update.new_username else None
        }
    
    return {"success": False, "message": "Nessuna modifica richiesta"}

@api_router.post("/admin/associate-license")
async def associate_license_to_admin(license_key: str, username: str = Depends(verify_token)):
    """Associa una licenza all'account admin corrente"""
    # Verifica che la licenza esista ed sia valida
    license_doc = await db.licenses.find_one({"license_key": license_key})
    
    if not license_doc:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    if license_doc['status'] != "active":
        raise HTTPException(status_code=403, detail="Licenza non attiva")
    
    # Verifica scadenza
    expires_at = datetime.fromisoformat(license_doc['expires_at'])
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=403, detail="Licenza scaduta")
    
    # Associa licenza all'admin
    await db.admins.update_one(
        {"username": username},
        {"$set": {"license_key": license_key}}
    )
    
    return {
        "success": True,
        "message": "Licenza associata correttamente",
        "plan": license_doc['plan'],
        "expires_at": license_doc['expires_at']
    }

@api_router.get("/admin/my-license")
async def get_my_license(username: str = Depends(verify_token)):
    """Ottieni informazioni sulla propria licenza"""
    admin = await db.admins.find_one({"username": username})
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trovato")
    
    # Super admin ha accesso illimitato
    if admin.get("role") == "super_admin":
        return {
            "unlimited": True,
            "role": "super_admin"
        }
    
    license_key = admin.get("license_key")
    
    if not license_key:
        raise HTTPException(status_code=404, detail="Nessuna licenza associata")
    
    license_doc = await db.licenses.find_one({"license_key": license_key}, {"_id": 0})
    
    if not license_doc:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    # Calcola giorni rimanenti
    expires_at = datetime.fromisoformat(license_doc['expires_at'])
    now = datetime.now(timezone.utc)
    days_remaining = (expires_at - now).days
    
    return {
        **license_doc,
        "days_remaining": days_remaining,
        "is_expired": now > expires_at
    }

@api_router.get("/admin/license-info", response_model=LicenseInfo)
async def get_license_info(username: str = Depends(verify_token)):
    """Ottieni informazioni dettagliate sulla licenza per la dashboard"""
    admin = await db.admins.find_one({"username": username})
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trovato")
    
    # Super admin ha accesso illimitato
    if admin.get("role") == "super_admin":
        return LicenseInfo(
            has_license=True,
            unlimited=True,
            role="super_admin",
            status="active"
        )
    
    license_key = admin.get("license_key")
    
    if not license_key:
        return LicenseInfo(
            has_license=False,
            role=admin.get("role", "admin")
        )
    
    license_doc = await db.licenses.find_one({"license_key": license_key})
    
    if not license_doc:
        return LicenseInfo(
            has_license=False,
            role=admin.get("role", "admin")
        )
    
    # Calcola giorni rimanenti
    expires_at = datetime.fromisoformat(license_doc['expires_at'])
    now = datetime.now(timezone.utc)
    days_remaining = max(0, (expires_at - now).days)
    
    # Verifica se scaduta
    is_expired = now > expires_at
    status = "expired" if is_expired else license_doc.get('status', 'active')
    
    return LicenseInfo(
        has_license=True,
        license_key=license_key,
        plan=license_doc.get('plan'),
        expires_at=license_doc.get('expires_at'),
        days_remaining=days_remaining,
        status=status,
        unlimited=False,
        role=admin.get("role", "admin")
    )

@api_router.post("/super-admin/create-admin")
async def create_admin(admin_data: AdminCreate, username: str = Depends(verify_super_admin)):
    """Crea un nuovo admin (solo super admin)"""
    # Verifica che l'username non esista già
    existing = await db.admins.find_one({"username": admin_data.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username già esistente")
    
    # Hash password
    hashed_password = bcrypt.hashpw(admin_data.password.encode('utf-8'), bcrypt.gensalt())
    
    # Crea admin
    new_admin = {
        "id": str(uuid.uuid4()),
        "username": admin_data.username,
        "password": hashed_password,
        "role": admin_data.role,
        "license_key": None,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.admins.insert_one(new_admin)
    
    return {
        "success": True,
        "message": f"Admin '{admin_data.username}' creato con successo",
        "username": admin_data.username,
        "role": admin_data.role
    }

@api_router.get("/super-admin/admins")
async def list_admins(username: str = Depends(verify_super_admin)):
    """Lista tutti gli admin (solo super admin)"""
    admins = await db.admins.find({}, {"_id": 0, "password": 0}).to_list(None)
    
    # Aggiungi info licenza per ogni admin
    for admin in admins:
        if admin.get("role") == "super_admin":
            admin["license_info"] = "Unlimited"
        elif admin.get("license_key"):
            license_doc = await db.licenses.find_one({"license_key": admin["license_key"]})
            if license_doc:
                expires_at = datetime.fromisoformat(license_doc['expires_at'])
                days_remaining = max(0, (expires_at - datetime.now(timezone.utc)).days)
                admin["license_info"] = f"{license_doc['plan']} - {days_remaining} giorni"
            else:
                admin["license_info"] = "Nessuna licenza"
        else:
            admin["license_info"] = "Nessuna licenza"
    
    return admins

@api_router.post("/super-admin/assign-license")
async def assign_license(
    admin_username: str,
    license_key: str,
    username: str = Depends(verify_super_admin)
):
    """Assegna una licenza a un admin (solo super admin)"""
    # Verifica che l'admin esista
    admin = await db.admins.find_one({"username": admin_username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trovato")
    
    # Verifica che la licenza esista ed è disponibile
    license_doc = await db.licenses.find_one({"license_key": license_key})
    if not license_doc:
        raise HTTPException(status_code=404, detail="Licenza non trovata")
    
    # Verifica che la licenza non sia già assegnata
    existing_admin = await db.admins.find_one({"license_key": license_key})
    if existing_admin and existing_admin["username"] != admin_username:
        raise HTTPException(status_code=400, detail=f"Licenza già assegnata a {existing_admin['username']}")
    
    # Assegna licenza all'admin
    await db.admins.update_one(
        {"username": admin_username},
        {"$set": {"license_key": license_key}}
    )
    
    # Aggiorna la licenza con l'email dell'admin se disponibile
    await db.licenses.update_one(
        {"license_key": license_key},
        {"$set": {"assigned_to": admin_username}}
    )
    
    return {
        "success": True,
        "message": f"Licenza {license_key} assegnata a {admin_username}"
    }

@api_router.delete("/super-admin/unassign-license/{admin_username}")
async def unassign_license(admin_username: str, username: str = Depends(verify_super_admin)):
    """Rimuove la licenza da un admin (solo super admin)"""
    admin = await db.admins.find_one({"username": admin_username})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trovato")
    
    old_license = admin.get("license_key")
    
    # Rimuovi licenza dall'admin
    await db.admins.update_one(
        {"username": admin_username},
        {"$set": {"license_key": None}}
    )
    
    # Aggiorna la licenza
    if old_license:
        await db.licenses.update_one(
            {"license_key": old_license},
            {"$set": {"assigned_to": None}}
        )
    
    return {
        "success": True,
        "message": f"Licenza rimossa da {admin_username}"
    }

# ============================================
# SISTEMA FOTO SERATE
# ============================================

# WebSocket manager per notifiche real-time
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/photos")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@api_router.post("/admin/serata/create")
async def create_serata(serata_create: SerataCreate, username: str = Depends(verify_token)):
    """Crea una nuova serata e la cartella foto"""
    data_oggi = datetime.now().strftime("%Y-%m-%d")
    nome_completo = f"{serata_create.nome}_{data_oggi}"
    
    # Crea cartella nel PC locale
    base_path = Path(__file__).parent.parent / "Foto_Serate"
    base_path.mkdir(exist_ok=True)
    
    folder_path = base_path / nome_completo
    if folder_path.exists():
        raise HTTPException(status_code=400, detail="Serata già esistente per oggi")
    
    folder_path.mkdir(parents=True)
    
    serata = Serata(
        nome=serata_create.nome,
        data=data_oggi,
        folder_path=str(folder_path),
        display_time=serata_create.display_time
    )
    
    await db.serate.insert_one(serata.model_dump())
    
    return {
        "success": True,
        "serata_id": serata.id,
        "nome": nome_completo,
        "folder_path": str(folder_path)
    }

@api_router.get("/admin/serate")
async def get_serate(username: str = Depends(verify_token)):
    """Ottieni tutte le serate"""
    serate = await db.serate.find({}, {"_id": 0}).to_list(None)
    
    # Aggiungi conteggio foto
    for serata in serate:
        folder_path = Path(serata['folder_path'])
        if folder_path.exists():
            foto_count = len(list(folder_path.glob("*.jpg"))) + len(list(folder_path.glob("*.jpeg"))) + len(list(folder_path.glob("*.png")))
            serata['foto_count'] = foto_count
        else:
            serata['foto_count'] = 0
    
    return serate

@api_router.get("/admin/serata/{serata_id}")
async def get_serata(serata_id: str, username: str = Depends(verify_token)):
    """Ottieni dettagli serata"""
    serata = await db.serate.find_one({"id": serata_id}, {"_id": 0})
    if not serata:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    # Lista foto
    folder_path = Path(serata['folder_path'])
    fotos = []
    if folder_path.exists():
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            for foto in folder_path.glob(ext):
                fotos.append({
                    "filename": foto.name,
                    "size": foto.stat().st_size,
                    "created_at": datetime.fromtimestamp(foto.stat().st_ctime).isoformat()
                })
    
    serata['fotos'] = fotos
    return serata

@api_router.post("/admin/serata/{serata_id}/upload")
async def upload_photo(
    serata_id: str,
    file: UploadFile = File(...),
    username: str = Depends(verify_token)
):
    """Upload foto alla serata"""
    serata = await db.serate.find_one({"id": serata_id})
    if not serata:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    if not serata.get('active', True):
        raise HTTPException(status_code=400, detail="Serata non attiva")
    
    # Verifica tipo file
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo immagini permesse")
    
    # Salva foto
    folder_path = Path(serata['folder_path'])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"foto_{timestamp}_{file.filename}"
    file_path = folder_path / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Notifica via WebSocket
    await manager.broadcast({
        "type": "new_photo",
        "serata_id": serata_id,
        "filename": filename,
        "path": str(file_path)
    })
    
    return {
        "success": True,
        "filename": filename,
        "path": str(file_path)
    }

@api_router.get("/serata/{serata_id}/active")
async def get_active_serata(serata_id: str):
    """Endpoint pubblico per camera app - verifica serata attiva"""
    serata = await db.serate.find_one({"id": serata_id}, {"_id": 0})
    if not serata:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    if not serata.get('active', True):
        raise HTTPException(status_code=400, detail="Serata terminata")
    
    return {
        "active": True,
        "nome": serata['nome'],
        "data": serata['data']
    }

@api_router.post("/serata/{serata_id}/upload-public")
async def upload_photo_public(
    serata_id: str,
    file: UploadFile = File(...)
):
    """Upload pubblico da camera app (senza autenticazione)"""
    serata = await db.serate.find_one({"id": serata_id})
    if not serata:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    if not serata.get('active', True):
        raise HTTPException(status_code=400, detail="Serata terminata")
    
    # Verifica tipo file
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Solo immagini permesse")
    
    # Salva foto
    folder_path = Path(serata['folder_path'])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"foto_{timestamp}_{file.filename}"
    file_path = folder_path / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Notifica via WebSocket
    await manager.broadcast({
        "type": "new_photo",
        "serata_id": serata_id,
        "filename": filename,
        "path": str(file_path)
    })
    
    return {
        "success": True,
        "filename": filename
    }

@api_router.put("/admin/serata/{serata_id}/close")
async def close_serata(serata_id: str, username: str = Depends(verify_token)):
    """Chiudi serata e pulisci i dati dei cantanti/canzoni"""
    result = await db.serate.update_one(
        {"id": serata_id},
        {"$set": {"active": False, "closed_at": datetime.now(timezone.utc).isoformat()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    # Pulisci database cantanti e canzoni della serata corrente
    # Nota: questo elimina TUTTI i cantanti/canzoni perché non c'è associazione serata_id
    # Se vuoi mantenere storico, non eliminare
    deleted_singers = await db.singers.delete_many({})
    deleted_songs = await db.songs.delete_many({})
    
    logger.info(f"Serata {serata_id} chiusa. Eliminati {deleted_singers.deleted_count} cantanti e {deleted_songs.deleted_count} canzoni")
    
    return {
        "success": True, 
        "message": "Serata chiusa e database pulito",
        "deleted_singers": deleted_singers.deleted_count,
        "deleted_songs": deleted_songs.deleted_count
    }

@api_router.post("/admin/serata/{serata_id}/send-emails")
async def send_photos_email(
    serata_id: str,
    email_config: EmailConfig,
    username: str = Depends(verify_token)
):
    """Invia foto via email a tutti i cantanti con email"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    serata = await db.serate.find_one({"id": serata_id})
    if not serata:
        raise HTTPException(status_code=404, detail="Serata non trovata")
    
    # Ottieni cantanti con email
    singers = await db.singers.find({"email": {"$exists": True, "$ne": None, "$ne": ""}}, {"_id": 0}).to_list(None)
    
    if not singers:
        return {"success": True, "sent": 0, "message": "Nessun cantante con email"}
    
    # Lista foto
    folder_path = Path(serata['folder_path'])
    fotos = []
    if folder_path.exists():
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            fotos.extend(list(folder_path.glob(ext)))
    
    if not fotos:
        return {"success": True, "sent": 0, "message": "Nessuna foto da inviare"}
    
    sent_count = 0
    errors = []
    
    # Invia email a ogni cantante
    for singer in singers:
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config.sender_email
            msg['To'] = singer['email']
            msg['Subject'] = f"Foto Serata Karaoke - {serata['nome']} - {serata['data']}"
            
            body = f"""
Ciao {singer['nome']}!

Grazie per aver partecipato alla serata karaoke {serata['nome']} del {serata['data']}.

In allegato trovi tutte le foto della serata!

A presto!
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Allega foto (max 10 per email per non eccedere dimensione)
            for foto in fotos[:10]:
                with open(foto, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={foto.name}')
                    msg.attach(part)
            
            # Invia email
            server = smtplib.SMTP(email_config.smtp_server, email_config.smtp_port)
            server.starttls()
            server.login(email_config.sender_email, email_config.sender_password)
            server.send_message(msg)
            server.quit()
            
            sent_count += 1
        except Exception as e:
            errors.append(f"{singer['email']}: {str(e)}")
    
    return {
        "success": True,
        "sent": sent_count,
        "total": len(singers),
        "errors": errors if errors else None
    }

app.include_router(api_router)

# Serve static files (frontend build)
frontend_build_path = Path(__file__).parent.parent / "frontend" / "build"
if frontend_build_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_build_path / "static")), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve index.html per tutte le route non-API
        if not full_path.startswith("api"):
            index_file = frontend_build_path / "index.html"
            if index_file.exists():
                return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Not Found")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()