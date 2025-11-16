# 🔐 GUIDA: Reset Password Admin/SuperAdmin

## 📋 Hai 3 Script Disponibili

### 1. `reset-password-simple.py` ⭐ CONSIGLIATO
**Uso:** Reset veloce password superadmin  
**Comando:**
```bash
python3 reset-password-simple.py
```

**Cosa fa:**
- Resetta la password di `superadmin` a `superadmin123`
- Veloce e semplice
- Nessuna domanda

---

### 2. `reset-admin-password.py` ⭐⭐ COMPLETO
**Uso:** Gestione completa admin  
**Comando:**
```bash
python3 reset-admin-password.py
```

**Cosa fa:**
- Mostra tutti gli admin nel database
- Permette di:
  1. Resettare password `admin` → `admin123`
  2. Resettare password `superadmin` → `superadmin123`
  3. Resettare password personalizzata
  4. Creare nuovo admin

**Menu interattivo!**

---

### 3. `reset-superadmin-password.py` ⭐⭐⭐ DETTAGLIATO
**Uso:** Reset con log dettagliati  
**Comando:**
```bash
python3 reset-superadmin-password.py
```

**Cosa fa:**
- Reset password superadmin con log completi
- Mostra tutti i passaggi
- Verifica la connessione
- Conferma l'operazione

---

## 🚀 QUICK START (Più Veloce)

### Opzione A: Reset Superadmin (1 comando)
```bash
cd /app
python3 reset-password-simple.py
```

**Output:**
```
🔧 Reset Password Superadmin

✅ Password resettata con successo!

📝 Nuove credenziali:
   Username: superadmin
   Password: superadmin123
```

### Opzione B: Reset con Menu (più opzioni)
```bash
cd /app
python3 reset-admin-password.py
```

**Output:**
```
📋 Admin nel database:
----------------------------------------
1. Username: admin (Role: admin)
2. Username: superadmin (Role: superadmin)
----------------------------------------

Cosa vuoi fare?
1. Resettare password 'admin' (admin123)
2. Resettare password 'superadmin' (superadmin123)
3. Resettare password personalizzata
4. Creare nuovo admin
0. Esci

Scelta: 
```

---

## 🔧 PERSONALIZZARE LA PASSWORD

### Metodo 1: Modifica il file prima di eseguire

Apri `reset-password-simple.py` e modifica questa riga:

```python
# Cambia la password qui se vuoi
NUOVA_PASSWORD = "superadmin123"  # ← Cambia qui
```

Poi esegui:
```bash
python3 reset-password-simple.py
```

### Metodo 2: Usa lo script interattivo

```bash
python3 reset-admin-password.py
```

Scegli opzione `3` e inserisci:
- Username: `superadmin`
- Nuova password: `la_tua_password_sicura`

---

## 📝 CREDENZIALI DEFAULT

Dopo il reset, le credenziali sono:

### Admin (Host Karaoke)
```
Username: admin
Password: admin123
URL: https://astounding-buttercream-5d9ab5.netlify.app/admin/login
```

### SuperAdmin (Gestione Licenze)
```
Username: superadmin
Password: superadmin123
URL: https://astounding-buttercream-5d9ab5.netlify.app/super-admin
```

---

## 🆘 TROUBLESHOOTING

### Errore: "No module named 'motor'"

**Soluzione:**
```bash
cd /app/backend
pip install -r requirements.txt
```

O installa solo motor:
```bash
pip install motor bcrypt
```

### Errore: "ServerSelectionTimeoutError"

**Causa:** MongoDB Atlas blocca il tuo IP

**Soluzione:**
1. Vai su MongoDB Atlas Dashboard
2. Network Access → Add IP Address
3. Aggiungi: `0.0.0.0/0` (permetti tutti gli IP)
4. Salva e attendi 1-2 minuti

### Errore: "Authentication failed"

**Causa:** Password MongoDB errata nell'URL

**Soluzione:**
Verifica che l'URL nel file sia corretto:
```
mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/...
```

### Password resettata ma login non funziona

**Possibili cause:**
1. Backend su Render non è aggiornato/connesso
2. Cache browser
3. Stai usando l'URL sbagliato

**Soluzioni:**
1. Riavvia il backend su Render
2. Apri in incognito/privato
3. Verifica l'URL: usa quello Netlify, non localhost

---

## 🔍 VERIFICA ADMIN NEL DATABASE

Vuoi solo vedere chi c'è nel database?

**Usa:**
```bash
python3 reset-admin-password.py
```

Poi scegli opzione `0` per uscire senza modifiche.

Vedrai la lista di tutti gli admin.

---

## 💡 ESEMPI PRATICI

### Esempio 1: Reset veloce superadmin
```bash
python3 reset-password-simple.py
# Password resettata a: superadmin123
```

### Esempio 2: Reset con password personalizzata
```bash
python3 reset-admin-password.py
# Scegli 3
# Username: superadmin
# Password: MiaPasswordSicura2025!
```

### Esempio 3: Creare nuovo super admin
```bash
python3 reset-admin-password.py
# Scegli 4
# Username: fabio
# Password: Fabio2025Secure!
# Role: 2 (superadmin)
```

---

## 📊 QUALE SCRIPT USARE?

| Situazione | Script Consigliato |
|------------|-------------------|
| Reset veloce superadmin | `reset-password-simple.py` |
| Reset con password custom | `reset-admin-password.py` |
| Creare nuovo admin | `reset-admin-password.py` |
| Vedere tutti gli admin | `reset-admin-password.py` |
| Debug completo | `reset-superadmin-password.py` |

---

## ⚠️ IMPORTANTE

1. **Cambia la password dopo il primo login!**
2. **Non usare password semplici in produzione**
3. **Gli script si connettono DIRETTAMENTE a MongoDB Atlas**
4. **Le modifiche sono IMMEDIATE**

---

## 🎯 DOPO IL RESET

1. Testa il login su Netlify
2. Cambia la password dall'interfaccia web
3. Salva le nuove credenziali in un posto sicuro

---

## 📞 SUPPORTO

Se gli script non funzionano:

1. Verifica di essere in `/app/`
2. Controlla che `motor` e `bcrypt` siano installati
3. Verifica Network Access su MongoDB Atlas
4. Controlla che l'URL MongoDB sia corretto

---

**Data:** 2025  
**Versione:** 1.0
