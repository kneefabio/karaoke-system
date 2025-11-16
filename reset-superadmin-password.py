#!/usr/bin/env python3
"""
Script per resettare la password del superadmin su MongoDB Atlas
"""

import sys
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Configurazione MongoDB Atlas
MONGO_URL = "mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing"
DB_NAME = "karaoke_db"

# Nuova password (puoi cambiarla qui)
NEW_PASSWORD = "superadmin123"

async def reset_superadmin_password():
    """
    Resetta la password del superadmin nel database
    """
    print("=" * 60)
    print("  RESET PASSWORD SUPERADMIN - KARAOKE SYSTEM")
    print("=" * 60)
    print()
    
    # Connessione a MongoDB
    print("📡 Connessione a MongoDB Atlas...")
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        # Test connessione
        await client.admin.command('ping')
        print("✅ Connessione riuscita!\n")
    except Exception as e:
        print(f"❌ ERRORE connessione: {e}")
        print("\nVerifica:")
        print("1. MongoDB Atlas Network Access permette il tuo IP")
        print("2. URL MongoDB è corretto")
        print("3. Password MongoDB è corretta")
        return
    
    # Cerca l'utente superadmin
    print("🔍 Ricerca utente 'superadmin'...")
    try:
        admin = await db.admins.find_one({"username": "superadmin"})
        
        if admin:
            print(f"✅ Utente trovato: {admin.get('username')}")
            print(f"   Role: {admin.get('role')}")
            print(f"   ID: {admin.get('id')}\n")
        else:
            print("⚠️  Utente 'superadmin' non trovato nel database")
            print("   Creo un nuovo utente superadmin...\n")
            
            # Crea nuovo superadmin
            import uuid
            admin = {
                "id": str(uuid.uuid4()),
                "username": "superadmin",
                "role": "superadmin"
            }
    except Exception as e:
        print(f"❌ ERRORE ricerca utente: {e}")
        return
    
    # Hash della nuova password
    print(f"🔐 Generazione hash per nuova password: '{NEW_PASSWORD}'")
    hashed_password = bcrypt.hashpw(NEW_PASSWORD.encode('utf-8'), bcrypt.gensalt())
    print("✅ Hash generato\n")
    
    # Aggiorna/Inserisci nel database
    print("💾 Aggiornamento database...")
    try:
        result = await db.admins.update_one(
            {"username": "superadmin"},
            {
                "$set": {
                    "username": admin["username"],
                    "password": hashed_password,
                    "role": admin["role"],
                    "id": admin.get("id")
                }
            },
            upsert=True
        )
        
        if result.modified_count > 0:
            print("✅ Password aggiornata con successo!")
        elif result.upserted_id:
            print("✅ Nuovo utente superadmin creato con successo!")
        else:
            print("⚠️  Nessuna modifica effettuata (password già uguale?)")
        
    except Exception as e:
        print(f"❌ ERRORE aggiornamento: {e}")
        return
    
    # Verifica finale
    print("\n🔍 Verifica finale...")
    try:
        updated_admin = await db.admins.find_one({"username": "superadmin"})
        
        # Test password
        if bcrypt.checkpw(NEW_PASSWORD.encode('utf-8'), updated_admin['password']):
            print("✅ Password verificata correttamente!\n")
        else:
            print("⚠️  Password non corrisponde (errore inatteso)\n")
            
    except Exception as e:
        print(f"⚠️  Errore verifica: {e}\n")
    
    # Chiudi connessione
    client.close()
    
    # Riepilogo
    print("=" * 60)
    print("  RESET COMPLETATO")
    print("=" * 60)
    print()
    print("📝 Credenziali aggiornate:")
    print(f"   Username: superadmin")
    print(f"   Password: {NEW_PASSWORD}")
    print()
    print("🌐 Prova ad accedere su:")
    print("   https://astounding-buttercream-5d9ab5.netlify.app/super-admin")
    print()
    print("=" * 60)

async def list_all_admins():
    """
    Mostra tutti gli admin nel database (per debug)
    """
    print("\n📋 Lista di tutti gli admin nel database:")
    print("-" * 60)
    
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        admins = await db.admins.find({}).to_list(None)
        
        if not admins:
            print("⚠️  Nessun admin trovato nel database")
        else:
            for admin in admins:
                print(f"\n👤 Username: {admin.get('username')}")
                print(f"   Role: {admin.get('role')}")
                print(f"   ID: {admin.get('id')}")
                print(f"   Password hash: {admin.get('password', b'')[:30]}...")
        
        client.close()
        print("\n" + "-" * 60)
        
    except Exception as e:
        print(f"❌ Errore: {e}")

def main():
    """
    Main function
    """
    print()
    print("Vuoi vedere la lista di tutti gli admin prima? (s/n)")
    choice = input("Scelta: ").lower().strip()
    
    if choice in ['s', 'si', 'y', 'yes']:
        asyncio.run(list_all_admins())
        print()
    
    print("Procedere con il reset della password del superadmin? (s/n)")
    confirm = input("Conferma: ").lower().strip()
    
    if confirm in ['s', 'si', 'y', 'yes']:
        asyncio.run(reset_superadmin_password())
    else:
        print("\n❌ Operazione annullata")
        sys.exit(0)

if __name__ == "__main__":
    main()
