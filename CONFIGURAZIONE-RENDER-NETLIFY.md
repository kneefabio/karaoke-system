# 🚀 GUIDA COMPLETA: Configurazione Render + Netlify

## 📊 I TUOI DATI

```
✅ MongoDB Atlas: mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing
✅ Backend Render: https://karaoke-backend-g48m.onrender.com
✅ Frontend Netlify: https://astounding-buttercream-5d9ab5.netlify.app/
```

---

## 🔧 PARTE 1: CONFIGURAZIONE RENDER (BACKEND)

### Passo 1: Accedi a Render Dashboard
1. Vai su: https://dashboard.render.com
2. Seleziona il servizio **"karaoke-backend"**

### Passo 2: Configura le Environment Variables
1. Clicca su **"Environment"** nel menu a sinistra
2. Clicca su **"Add Environment Variable"**
3. Aggiungi le seguenti variabili **UNA PER UNA**:

#### Variable 1: MONGO_URL
```
Key: MONGO_URL
Value: mongodb+srv://kneefabio_db_user:Kneefa4281-020480@karaokelicensing.evsiclb.mongodb.net/?appName=KaraokeLicensing
```

#### Variable 2: DB_NAME
```
Key: DB_NAME
Value: karaoke_db
```

#### Variable 3: CORS_ORIGINS
```
Key: CORS_ORIGINS
Value: https://astounding-buttercream-5d9ab5.netlify.app,https://karaoke-backend-g48m.onrender.com
```

#### Variable 4: JWT_SECRET
```
Key: JWT_SECRET
Value: karaoke_production_secret_key_2025_fabio_secure_token_987654321
```

### Passo 3: Salva e Rideploya
1. Clicca **"Save Changes"**
2. Render riavvierà automaticamente il servizio
3. Attendi che il deploy finisca (5-10 minuti)

### Passo 4: Verifica che il Backend Funzioni
Apri nel browser:
```
https://karaoke-backend-g48m.onrender.com/api/health
```

Dovresti vedere: `{"status":"ok"}` o una risposta simile

---

## 🎨 PARTE 2: CONFIGURAZIONE NETLIFY (FRONTEND)

### Passo 1: Accedi a Netlify Dashboard
1. Vai su: https://app.netlify.com
2. Seleziona il sito **"astounding-buttercream-5d9ab5"**

### Passo 2: Configura Environment Variables
1. Vai su **"Site settings"** → **"Environment variables"**
2. Clicca **"Add a variable"**
3. Aggiungi:

```
Key: REACT_APP_BACKEND_URL
Value: https://karaoke-backend-g48m.onrender.com
```

### Passo 3: Rideploya il Frontend
1. Vai su **"Deploys"**
2. Clicca **"Trigger deploy"** → **"Clear cache and deploy site"**
3. Attendi che il deploy finisca (2-3 minuti)

### Passo 4: Testa il Frontend
Apri: https://astounding-buttercream-5d9ab5.netlify.app/

---

## 🧪 PARTE 3: TEST DI FUNZIONAMENTO

### Test 1: Backend API
Apri in un browser o con curl:
```bash
curl https://karaoke-backend-g48m.onrender.com/api/health
```

**Risposta attesa:** 
```json
{"status":"ok"}
```

### Test 2: Login Admin
1. Vai su: https://astounding-buttercream-5d9ab5.netlify.app/admin/login
2. Credenziali default:
   - Username: `admin`
   - Password: `admin123`

**Se funziona:** Dovresti essere reindirizzato alla dashboard ✅

**Se NON funziona:** Vai al Troubleshooting sotto ⬇️

---

## 🔍 TROUBLESHOOTING

### Problema: "Network Error" o "Failed to fetch"

**Causa:** CORS non configurato correttamente

**Soluzione:**
1. Verifica su Render che `CORS_ORIGINS` includa esattamente:
   ```
   https://astounding-buttercream-5d9ab5.netlify.app,https://karaoke-backend-g48m.onrender.com
   ```
2. Nessuno spazio prima/dopo le virgole
3. Usa HTTPS, non HTTP

### Problema: "Invalid credentials" anche con password corretta

**Causa:** Database vuoto o non connesso

**Soluzione:**
1. Verifica che `MONGO_URL` su Render sia corretto
2. Controlla i logs su Render:
   - Dashboard → Logs
   - Cerca errori tipo "MongoServerError" o "connection refused"

### Problema: Backend non risponde

**Causa:** Servizio non attivo su Render (free tier si spegne dopo inattività)

**Soluzione:**
1. Vai su Render Dashboard
2. Verifica che lo status sia "Live" (verde)
3. Se è "Sleeping", fai una richiesta per svegliarlo
4. Attendi 30-60 secondi

### Problema: "502 Bad Gateway" su Render

**Causa:** Backend ha crashato all'avvio

**Soluzione:**
1. Vai su Render → Logs
2. Cerca l'errore specifico
3. Probabilmente è un problema con MONGO_URL malformato

---

## 📝 CHECKLIST FINALE

Prima di testare, verifica che:

### Su Render:
- [ ] MONGO_URL configurato correttamente (con password completa)
- [ ] DB_NAME = karaoke_db
- [ ] CORS_ORIGINS include il tuo URL Netlify
- [ ] JWT_SECRET configurato
- [ ] Servizio in stato "Live" (verde)
- [ ] Logs non mostrano errori

### Su Netlify:
- [ ] REACT_APP_BACKEND_URL = https://karaoke-backend-g48m.onrender.com
- [ ] Deploy completato con successo
- [ ] Frontend carica senza errori nella console

### Test Finale:
- [ ] Backend risponde a /api/health
- [ ] Frontend si apre correttamente
- [ ] Login admin funziona
- [ ] QR code booking funziona

---

## 🎯 CREDENZIALI DI DEFAULT

Dopo il primo deploy, il sistema crea automaticamente:

### Admin (Host Karaoke)
```
Username: admin
Password: admin123
```

### Super Admin (Gestione Licenze)
```
Username: superadmin
Password: superadmin123
```

⚠️ **IMPORTANTE:** Cambia queste password dopo il primo login usando l'endpoint:
```
POST /api/admin/credentials
```

---

## 📞 SUPPORTO

Se dopo aver seguito tutti i passi continua a non funzionare:

1. Controlla i **Logs di Render** per errori backend
2. Apri la **Console del Browser** (F12) per errori frontend
3. Verifica che MongoDB Atlas permetta connessioni da qualsiasi IP:
   - Vai su MongoDB Atlas → Network Access
   - Aggiungi IP: `0.0.0.0/0` (permette tutti gli IP)

---

**Data:** 2025
**Versione:** 1.0 - Configurazione Produzione
