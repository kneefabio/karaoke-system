# 🎤 SISTEMA KARAOKE COMPLETO

Sistema professionale di prenotazioni karaoke con foto real-time e gestione licenze.

## ✅ QUICK START LOCALE

### Avvio Tutto Insieme:

```cmd
start-karaoke-complete.bat
```

Questo avvia:
- ✅ Backend (FastAPI + MongoDB)
- ✅ Frontend (React)  
- ✅ Photo Overlay (Electron)

Browser si apre automaticamente su http://localhost:3000

---

## 🔧 PROBLEMI RISOLTI

### ✅ Login ora funziona
- Frontend configurato per localhost
- Backend risponde correttamente

### ✅ Electron Overlay connesso
- WebSocket usa IPv4 (127.0.0.1)
- Niente più errori ECONNREFUSED

### ✅ Deploy Cloud configurato
- Render: Backend
- Netlify: Frontend
- MongoDB Atlas: Database

---

## 🚀 DEPLOY CLOUD

### Segui questa guida:
📖 **GUIDA-DEPLOY-CLOUD.txt**

Passi principali:
1. Crea MongoDB Atlas (gratis)
2. Deploy backend su Render (gratis)
3. Deploy frontend su Netlify (gratis)
4. Aggiorna CORS
5. Sistema online! 🌐

**Quando pronto, fornisci:**
- MongoDB connection string
- GitHub repository URL

E ti aiuto con il deploy automatico!

---

## 📁 FILE PRINCIPALI

### Script Avvio:
- `start-karaoke-complete.bat` ← **USA QUESTO!**
- `start-server-online.bat` - Solo backend
- `start-overlay.bat` - Solo overlay
- `start-ngrok.bat` - Esposizione remota

### Guide:
- `GUIDA-DEPLOY-CLOUD.txt` - Deploy Render + Netlify
- `GUIDA-LICENSING.txt` - Sistema licenze
- `GUIDA-SISTEMA-FOTO.txt` - Sistema foto
- `TEST-SISTEMA-FOTO.txt` - Test completo

### Configurazione:
- `backend/.env` - Locale
- `backend/.env.production` - Cloud
- `frontend/.env` - Locale  
- `frontend/.env.production` - Cloud
- `render.yaml` - Config Render
- `netlify.toml` - Config Netlify

---

## 🎯 FUNZIONALITÀ

### Sistema Base:
✅ Form prenotazione pubblico
✅ Dashboard admin real-time
✅ Codici univoci progressivi (001, 002...)
✅ Gestione canzoni cantate
✅ Reset/pulizia serata

### Sistema Licenze:
✅ 3 piani: 1 sera (€14.90), 1 mese (€39.90), 1 anno (€129.90)
✅ Super Admin Panel gestione licenze
✅ Verifica licenza automatica
✅ Username/password modificabili
✅ Email nel form prenotazione

### Sistema Foto:
✅ Creazione serate con QR code
✅ Camera app smartphone (4G/5G)
✅ Upload foto real-time
✅ Electron overlay con animazioni
✅ 8 animazioni entrata casuali
✅ 7 animazioni uscita casuali
✅ WebSocket sincronizzazione
✅ Invio email automatico con foto

---

## 🔑 ACCESSI DEFAULT

### Admin Dashboard:
- URL: http://localhost:3000/admin/login
- User: `admin`
- Pass: `admin123`

### Super Admin:
- URL: http://localhost:3000/super-admin
- User: `superadmin`
- Pass: `superadmin123`

⚠️ **CAMBIARE IN PRODUZIONE!**

---

## 📊 ARCHITETTURA

### LOCALE (PC):
```
PC Windows
├── MongoDB (locale)
├── Backend FastAPI :8001
├── Frontend React :3000
├── Electron Overlay (fullscreen)
└── Foto salvate in: /app/Foto_Serate/
```

### CLOUD (Produzione):
```
Internet
├── Netlify (Frontend)
│   └── https://tuoapp.netlify.app
├── Render (Backend)
│   └── https://tuoapp.onrender.com
└── MongoDB Atlas (Database)
    └── cluster.mongodb.net
```

### IBRIDO (Raccomandato):
```
Backend/Frontend su Cloud (Render + Netlify)
    ↓
Cliente locale avvia solo Electron Overlay
    ↓
Overlay si connette a backend cloud via WebSocket
    ↓
Foto mostrate real-time con animazioni
```

---

## 💰 MONETIZZAZIONE

### Piani Tariffari:
- 🎤 1 Sera: €14.90 (24h)
- 📅 1 Mese: €39.90 (30 giorni)
- ⭐ 1 Anno: €129.90 (365 giorni)

### Super Admin:
- Crea licenze
- Attiva/sospendi
- Estendi scadenze
- Statistiche vendite

---

## 🧪 TEST

### Test Locale Completo:

1. Avvia: `start-karaoke-complete.bat`
2. Browser: http://localhost:3000/admin/serate
3. Crea serata
4. Scannerizza QR con smartphone
5. Scatta foto
6. Foto appare su overlay! ✨

Segui: **TEST-SISTEMA-FOTO.txt** per test dettagliato

---

## 🌐 DEPLOY CLOUD

### Pronto per deploy?

Fornisci questi dati:

1. **MongoDB Atlas:**
   - Connection string: `mongodb+srv://...`

2. **GitHub:**
   - Repository URL: `https://github.com/...`

Poi eseguo deploy automatico su:
- ✅ Render (backend)
- ✅ Netlify (frontend)
- ✅ MongoDB Atlas (database)

**Costo:** €0/mese (tier gratuiti)

---

## 📞 SUPPORTO

### Per problemi:

1. Verifica MongoDB attivo
2. Check log backend
3. Riavvia sistema
4. Segui guide specifiche

### File log:
- Backend: `/var/log/supervisor/backend.*.log`
- Frontend: Console browser (F12)
- Overlay: Terminale dove hai avviato

---

## 🎉 RIEPILOGO

### Sistema Completo Include:

✅ Prenotazioni karaoke (codici univoci)
✅ Dashboard admin real-time
✅ Sistema licenze (3 piani vendita)
✅ Super Admin Panel
✅ Gestione serate foto
✅ Camera app smartphone
✅ Electron overlay animato
✅ Invio email automatico
✅ Deploy cloud ready
✅ Script avvio unificato

### Pronto per:
- 🏠 Uso locale (PC)
- 🌐 Deploy cloud (Render + Netlify)
- 💰 Vendita con licenze
- 🎤 Eventi karaoke professionali

---

**Sistema 100% completo e funzionante! 🎊**

Per iniziare: `start-karaoke-complete.bat`

Buon karaoke! 🎤✨📸
