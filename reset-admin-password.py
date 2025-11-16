#!/usr/bin/env python3
"""
Script per resettare QUALSIASI password admin/superadmin
Esegui: python3 reset-admin-password.py
"""

import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Configurazione MongoDB
MONGO_URL = "mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing"
DB_NAME = "karaoke_db"

async def list_admins():
    """Mostra tutti gli admin"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("\n📋 Admin nel database:")
    print("-" * 40)
    
    admins = await db.admins.find({}).to_list(None)
    
    if not admins:
        print("⚠️  Nessun admin trovato")
        return []
    
    for i, admin in enumerate(admins, 1):
        print(f"{i}. Username: {admin.get('username')} (Role: {admin.get('role')})")
    
    print("-" * 40)
    client.close()
    return admins

async def reset_password(username, new_password):
    """Resetta la password di un utente"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Hash password
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    # Aggiorna
    result = await db.admins.update_one(
        {"username": username},
        {"$set": {"password": hashed}}
    )
    
    client.close()
    
    if result.modified_count > 0:
        print(f"\n✅ Password resettata!")
        print(f"   Username: {username}")
        print(f"   Nuova password: {new_password}\n")
        return True
    else:
        print(f"\n❌ Utente '{username}' non trovato\n")
        return False

async def create_new_admin(username, password, role):
    """Crea un nuovo admin"""
    import uuid
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Crea
    await db.admins.insert_one({
        "id": str(uuid.uuid4()),
        "username": username,
        "password": hashed,
        "role": role
    })
    
    client.close()
    print(f"\n✅ Nuovo admin creato!")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   Role: {role}\n")

async def main():
    print("\n" + "=" * 50)
    print("  GESTIONE PASSWORD ADMIN - KARAOKE SYSTEM")
    print("=" * 50)
    
    # Mostra admin esistenti
    admins = await list_admins()
    
    print("\nCosa vuoi fare?")
    print("1. Resettare password 'admin' (admin123)")
    print("2. Resettare password 'superadmin' (superadmin123)")
    print("3. Resettare password personalizzata")
    print("4. Creare nuovo admin")
    print("0. Esci")
    
    choice = input("\nScelta: ").strip()
    
    if choice == "1":
        await reset_password("admin", "admin123")
    
    elif choice == "2":
        await reset_password("superadmin", "superadmin123")
    
    elif choice == "3":
        username = input("\nUsername: ").strip()
        password = input("Nuova password: ").strip()
        if username and password:
            await reset_password(username, password)
        else:
            print("❌ Username e password obbligatori")
    
    elif choice == "4":
        username = input("\nUsername: ").strip()
        password = input("Password: ").strip()
        print("Role:")
        print("1. admin (host karaoke)")
        print("2. superadmin (gestione licenze)")
        role_choice = input("Scelta: ").strip()
        
        role = "superadmin" if role_choice == "2" else "admin"
        
        if username and password:
            await create_new_admin(username, password, role)
        else:
            print("❌ Username e password obbligatori")
    
    elif choice == "0":
        print("\n👋 Ciao!\n")
    
    else:
        print("\n❌ Scelta non valida\n")

if __name__ == "__main__":
    asyncio.run(main())
