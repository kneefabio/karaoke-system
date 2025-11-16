# Configurazione File Environment (.env)

Questo documento spiega la struttura dei file di configurazione del progetto.

## 📁 Struttura File

### Backend

1. **`.env.template`** ✅ VERSIONATO
   - Template per ambiente locale
   - Copia questo file in `.env` per sviluppo locale

2. **`.env`** ❌ NON VERSIONATO (gitignore)
   - Configurazione locale per sviluppo
   - MongoDB locale: `mongodb://localhost:27017`
   - CORS: `*` (permetti tutto in locale)

3. **`.env.production.template`** ✅ VERSIONATO
   - Template per produzione
   - Copia questo file in `.env.production` per deploy su Render

4. **`.env.production`** ❌ NON VERSIONATO (gitignore)
   - Configurazione per deployment su Render
   - MongoDB Atlas con credenziali reali
   - CORS limitato ai domini di produzione

### Frontend

1. **`.env.template`** ✅ VERSIONATO
   - Template per ambiente locale
   - Copia questo file in `.env` per sviluppo locale

2. **`.env`** ❌ NON VERSIONATO (gitignore)
   - URL backend locale: `http://localhost:8001` o URL preview Emergent

3. **`.env.production.template`** ✅ VERSIONATO
   - Template per produzione
   - Copia questo file in `.env.production` per deploy su Netlify

4. **`.env.production`** ❌ NON VERSIONATO (gitignore)
   - URL backend produzione: il tuo dominio Render

## 🚀 Come Usare

### Per Sviluppo Locale

1. Copia i template:
   ```bash
   # Backend
   cp backend/.env.template backend/.env
   
   # Frontend
   cp frontend/.env.template frontend/.env
   ```

2. Modifica i file `.env` con i tuoi valori locali

### Per Produzione (Deploy)

1. Copia i template production:
   ```bash
   # Backend
   cp backend/.env.production.template backend/.env.production
   
   # Frontend
   cp frontend/.env.production.template frontend/.env.production
   ```

2. Modifica con le credenziali reali:
   - MongoDB Atlas URL
   - Domini reali per CORS
   - JWT Secret sicuro
   - URL backend su Render

## ⚠️ Sicurezza

- **MAI** committare file `.env` o `.env.production` reali su GitHub
- Solo i file `.template` devono essere versionati
- Cambia sempre `JWT_SECRET` in produzione
- Usa password forti per MongoDB Atlas

## 📝 Variabili Richieste

### Backend
- `MONGO_URL`: URL connessione MongoDB
- `DB_NAME`: Nome database
- `CORS_ORIGINS`: Domini permessi
- `JWT_SECRET`: Chiave per token autenticazione
- `PORT`: Porta server (default: 8001)

### Frontend
- `REACT_APP_BACKEND_URL`: URL del backend API
