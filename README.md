# Sistema Prenotazioni Karaoke 🎤

Sistema completo per gestire prenotazioni di canzoni per karaoke con dashboard amministrativa in tempo reale.

## 🌟 Caratteristiche

### Pagina Pubblica
- Form prenotazione intuitivo (nome, canzone, tonalità)
- Sistema di codici progressivi univoci (001, 002, 003...)
- Verifica automatica nome/codice per prenotazioni multiple
- Design responsive e professionale
- Messaggi di errore e conferma immediati

### Dashboard Amministratore
- Login protetto (JWT authentication)
- Statistiche in tempo reale:
  - Totale cantanti
  - Totale prenotazioni
  - Canzoni cantate
  - Prenotazioni in attesa
- Gestione completa prenotazioni:
  - Visualizzazione per cantante con tutte le canzoni
  - Numeri d'ordine progressivi
  - Marcare canzoni come cantate
  - Eliminare canzoni o cantanti
- Toggle per chiudere/aprire prenotazioni
- Aggiornamento automatico ogni 3 secondi

## 🚀 Installazione Automatica

### Prerequisiti
- Python 3.11 o superiore
- Node.js 18 o superiore
- MongoDB Community Edition
- Yarn (verrà installato automaticamente se mancante)

### Windows
```cmd
setup.bat
```

### Mac/Linux
```bash
chmod +x setup.sh
./setup.sh
```

Lo script installerà automaticamente tutte le dipendenze e configurerà l'ambiente.

## 🎯 Avvio del Sistema

### Avvio Completo (Raccomandato)

**Windows:**
```cmd
start-all.bat
```

**Mac/Linux:**
```bash
./start-all.sh
```

Questo avvierà automaticamente backend e frontend.

### Avvio Manuale Separato

**Backend:**
```bash
# Windows
start-backend.bat

# Mac/Linux
./start-backend.sh
```

**Frontend:**
```bash
# Windows
start-frontend.bat

# Mac/Linux
./start-frontend.sh
```

**MongoDB:**
```bash
# Mac/Linux
mongod --dbpath ~/data/db

# Windows
mongod --dbpath %USERPROFILE%\data\db

# Oppure avvia come servizio se installato
```

## 🌐 Accesso

Dopo l'avvio, il sistema sarà disponibile su:

- **Frontend (Pagina Pubblica):** http://localhost:3000
- **Backend API:** http://localhost:8001
- **Documentazione API Interattiva:** http://localhost:8001/docs
- **Admin Dashboard:** http://localhost:3000/admin/dashboard

### Credenziali Admin
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Importante:** Cambia la password admin in produzione modificando il file `backend/server.py`

## 📁 Struttura del Progetto

```
.
├── backend/
│   ├── server.py          # API FastAPI
│   ├── requirements.txt   # Dipendenze Python
│   └── .env              # Configurazione ambiente
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── BookingPage.jsx      # Form prenotazione pubblica
│   │   │   ├── AdminLogin.jsx       # Login amministratore
│   │   │   └── AdminDashboard.jsx   # Dashboard admin
│   │   ├── components/ui/           # Componenti UI Shadcn
│   │   ├── App.js                   # Root component
│   │   └── App.css                  # Stili globali
│   ├── package.json       # Dipendenze Node.js
│   └── .env              # Configurazione frontend
├── setup.sh              # Script installazione Linux/Mac
├── setup.bat             # Script installazione Windows
├── start-all.sh          # Avvio completo Linux/Mac
├── start-all.bat         # Avvio completo Windows
└── README.md             # Questa documentazione
```

## 🔧 Stack Tecnologico

### Backend
- **FastAPI** - Framework API REST moderno e veloce
- **MongoDB** - Database NoSQL per flessibilità
- **Motor** - Driver MongoDB asincrono
- **PyJWT** - Autenticazione JWT
- **Bcrypt** - Hashing password sicuro
- **Pydantic** - Validazione dati

### Frontend
- **React 19** - UI library moderna
- **React Router** - Navigazione SPA
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/UI** - Componenti UI accessibili
- **Lucide React** - Icone moderne
- **Sonner** - Toast notifications eleganti

## 📖 Utilizzo

### Flusso Cliente

1. Il cliente scansiona il QR code (che punta a `http://localhost:3000` in locale)
2. Compila il form con:
   - **Codice** (opzionale): se ha già prenotato prima
   - **Nome**: il suo nome
   - **Canzone**: titolo della canzone
   - **Tonalità**: es. Do, Re, originale, +1, -2
3. Clicca "Invia Prenotazione"
4. Riceve il codice univoco da ricordare per future prenotazioni

### Flusso Amministratore

1. Accede a `/admin/login`
2. Inserisce credenziali (admin/admin123)
3. Visualizza la dashboard con:
   - Statistiche in tempo reale
   - Lista cantanti con tutte le loro canzoni
   - Numeri d'ordine per ogni canzone
4. Può:
   - Marcare canzoni come cantate (✓)
   - Eliminare canzoni singole
   - Eliminare cantanti con tutte le loro canzoni
   - Chiudere/aprire le prenotazioni con toggle

## 🔒 Sicurezza

- Password admin hashata con bcrypt
- Autenticazione JWT per API protette
- Validazione input lato backend
- CORS configurato correttamente
- Verifica nome/codice per prevenire prenotazioni false

⚠️ **Per produzione:**
1. Cambia `JWT_SECRET` in `backend/.env`
2. Cambia password admin di default
3. Usa HTTPS
4. Configura CORS_ORIGINS con dominio specifico
5. Usa MongoDB Atlas o server dedicato

## 🐛 Troubleshooting

### MongoDB non si avvia
```bash
# Crea la directory dati
mkdir -p ~/data/db  # Mac/Linux
mkdir %USERPROFILE%\data\db  # Windows

# Avvia con percorso specifico
mongod --dbpath ~/data/db
```

### Porta già in uso
Se le porte 3000 o 8001 sono occupate:

**Backend** - modifica `start-backend.sh/bat` cambiando `--port 8001`
**Frontend** - modifica `package.json` aggiungendo `"start": "PORT=3001 react-scripts start"`

### Errore CORS
Verifica che `backend/.env` contenga:
```
CORS_ORIGINS=http://localhost:3000
```

### Frontend non si connette al backend
Verifica che `frontend/.env` contenga:
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 📝 API Endpoints

### Pubblici
- `GET /api/` - Health check
- `POST /api/book` - Crea prenotazione
- `GET /api/settings` - Ottieni stato prenotazioni

### Admin (richiedono token JWT)
- `POST /api/admin/login` - Login admin
- `GET /api/admin/singers` - Lista cantanti con canzoni
- `GET /api/admin/stats` - Statistiche sistema
- `PUT /api/admin/song/{id}` - Modifica canzone
- `DELETE /api/admin/song/{id}` - Elimina canzone
- `DELETE /api/admin/singer/{id}` - Elimina cantante
- `PUT /api/admin/settings` - Aggiorna impostazioni

Documentazione interattiva completa: http://localhost:8001/docs

## 🎨 Personalizzazione

### Colori e Stile
Modifica `frontend/src/App.css` e i componenti in `frontend/src/pages/`

### Database
Il database MongoDB si chiama `karaoke_db` e contiene le collection:
- `singers` - Cantanti con codici univoci
- `songs` - Prenotazioni canzoni
- `settings` - Configurazione sistema
- `admins` - Utenti amministratori

## 📄 Licenza

Progetto creato per uso personale/commerciale.

## 🤝 Supporto

Per problemi o domande, consulta la documentazione API su `/docs` o controlla i log:
- Backend: console dove hai avviato il backend
- Frontend: console browser (F12)
- MongoDB: file di log MongoDB

---

**Buon divertimento con il tuo sistema Karaoke! 🎤🎵**
