from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
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

ROOT_DIR = Path(__file__).parent
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
    else:
        # Create new singer
        codice = await get_next_codice()
        singer = Singer(nome=booking.nome, codice=codice)
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
    
    if not bcrypt.checkpw(login.password.encode('utf-8'), admin['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    
    access_token = create_access_token(data={"sub": login.username})
    return LoginResponse(access_token=access_token)

@api_router.get("/admin/singers", response_model=List[SingerWithSongs])
async def get_singers(username: str = Depends(verify_token)):
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
async def get_stats(username: str = Depends(verify_token)):
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
async def update_song(song_id: str, update: UpdateSongRequest, username: str = Depends(verify_token)):
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