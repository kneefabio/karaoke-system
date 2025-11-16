#!/usr/bin/env python3
"""Reset entrambi gli admin (admin + superadmin)"""

import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

MONGO_URL = "mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing"
DB_NAME = "karaoke_db"

async def reset_both():
    print("\n🔧 Reset Password Admin + SuperAdmin\n")
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Reset admin
    hashed_admin = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
    await db.admins.update_one(
        {"username": "admin"},
        {"$set": {"password": hashed_admin}},
        upsert=True
    )
    print("✅ Admin password resettata → admin123")
    
    # Reset superadmin
    hashed_super = bcrypt.hashpw("superadmin123".encode('utf-8'), bcrypt.gensalt())
    await db.admins.update_one(
        {"username": "superadmin"},
        {"$set": {"password": hashed_super}},
        upsert=True
    )
    print("✅ SuperAdmin password resettata → superadmin123")
    
    print("\n📝 Credenziali:")
    print("   admin / admin123")
    print("   superadmin / superadmin123\n")
    
    client.close()

asyncio.run(reset_both())
