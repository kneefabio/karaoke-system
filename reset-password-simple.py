#!/usr/bin/env python3
"""
Script SEMPLICE per resettare password superadmin
Esegui: python3 reset-password-simple.py
"""

import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# ==================== CONFIGURAZIONE ====================
MONGO_URL = "mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing"
DB_NAME = "karaoke_db"

# Cambia la password qui se vuoi
NUOVA_PASSWORD = "superadmin123"
# ========================================================

async def reset_password():
    print("\n🔧 Reset Password Superadmin\n")
    
    # Connetti a MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Hash password
    hashed = bcrypt.hashpw(NUOVA_PASSWORD.encode('utf-8'), bcrypt.gensalt())
    
    # Aggiorna database
    result = await db.admins.update_one(
        {"username": "superadmin"},
        {"$set": {"password": hashed}},
        upsert=True
    )
    
    if result.modified_count > 0 or result.upserted_id:
        print(f"✅ Password resettata con successo!")
        print(f"\n📝 Nuove credenziali:")
        print(f"   Username: superadmin")
        print(f"   Password: {NUOVA_PASSWORD}\n")
    else:
        print("⚠️  Nessuna modifica effettuata\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(reset_password())
