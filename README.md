# Sistema Prenotazioni Karaoke 🎤

Sistema completo per gestire prenotazioni di canzoni per karaoke con dashboard amministrativa in tempo reale.

## 🌟 Cosa fa questo sistema

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

---

## 📥 GUIDA INSTALLAZIONE COMPLETA - PASSO PER PASSO

### PARTE 1: SCARICA E INSTALLA I PROGRAMMI NECESSARI

#### 🔹 Passo 1: Installa Python

**Windows:**
1. Vai su https://www.python.org/downloads/
2. Clicca sul grande pulsante giallo "Download Python 3.11.x"
3. Apri il file scaricato (es: `python-3.11.9-amd64.exe`)
4. ⚠️ **IMPORTANTE:** Spunta la casella "Add Python to PATH" in basso
5. Clicca "Install Now"
6. Aspetta che finisca l'installazione
7. Clicca "Close"

**Mac:**
1. Vai su https://www.python.org/downloads/
2. Clicca sul grande pulsante "Download Python 3.11.x"
3. Apri il file scaricato (es: `python-3.11.9-macos11.pkg`)
4. Segui la procedura guidata cliccando "Continua" e "Installa"
5. Inserisci la password del Mac quando richiesto
6. Clicca "Chiudi" quando finito

**Come verificare:**
1. Apri il Terminale (Mac) o Prompt dei comandi (Windows)
   - Windows: Premi tasto Windows, scrivi `cmd`, premi Invio
   - Mac: Premi Cmd+Spazio, scrivi `Terminal`, premi Invio
2. Scrivi: `python --version` e premi Invio
3. Dovresti vedere: `Python 3.11.x`

---

#### 🔹 Passo 2: Installa Node.js

**Windows e Mac:**
1. Vai su https://nodejs.org/
2. Clicca sul pulsante verde "LTS" (Recommended for Most Users)
3. Apri il file scaricato:
   - Windows: `node-v18.x.x-x64.msi`
   - Mac: `node-v18.x.x.pkg`
4. Segui la procedura guidata:
   - Clicca "Next" o "Continua" per ogni schermata
   - Accetta i termini di licenza
   - Clicca "Install" o "Installa"
5. Aspetta che finisca
6. Clicca "Finish" o "Chiudi"

**Come verificare:**
1. Apri un NUOVO Terminale/Prompt (chiudi quello vecchio e aprilo di nuovo)
2. Scrivi: `node --version` e premi Invio
3. Dovresti vedere: `v18.x.x`

---

#### 🔹 Passo 3: Installa MongoDB

**Windows:**
1. Vai su https://www.mongodb.com/try/download/community
2. Seleziona:
   - Version: 7.0.x (Current)
   - Platform: Windows
   - Package: msi
3. Clicca "Download"
4. Apri il file scaricato (es: `mongodb-windows-x86_64-7.0.x.msi`)
5. Clicca "Next" fino ad arrivare a "Service Configuration"
6. ⚠️ **IMPORTANTE:** Spunta "Install MongoDB as a Service"
7. Clicca "Next" e poi "Install"
8. Aspetta che finisca
9. Clicca "Finish"

**Mac:**
1. Apri il Terminale
2. Copia e incolla questo comando (tutto insieme) e premi Invio:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Segui le istruzioni (potrebbero chiederti la password)
4. Quando finito, scrivi:
   ```bash
   brew tap mongodb/brew
   ```
5. Premi Invio, aspetta che finisca
6. Poi scrivi:
   ```bash
   brew install mongodb-community
   ```
7. Premi Invio e aspetta (può richiedere alcuni minuti)

**Come verificare:**
1. Apri Terminale/Prompt
2. Scrivi: `mongod --version` e premi Invio
3. Dovresti vedere informazioni sulla versione di MongoDB

---

### PARTE 2: SCARICA IL PROGETTO KARAOKE

#### 🔹 Passo 4: Scarica i file del progetto

**Opzione A - Da Emergent (se hai salvato su GitHub):**
1. Vai su https://github.com
2. Accedi con il tuo account
3. Trova il repository del progetto
4. Clicca il pulsante verde "Code"
5. Clicca "Download ZIP"
6. Vai nella cartella Download
7. Fai click destro sul file ZIP → "Estrai tutto" (Windows) o doppio click (Mac)
8. Scegli dove estrarre (es: Documenti)

**Opzione B - Crea manualmente:**
1. Apri la tua piattaforma Emergent
2. Clicca sul pulsante "VS Code" per vedere tutti i file
3. Crea una cartella sul tuo computer (es: `Documenti/karaoke`)
4. Copia tutti i file e cartelle da Emergent in questa cartella locale

---

### PARTE 3: INSTALLA IL PROGETTO

#### 🔹 Passo 5: Vai nella cartella del progetto

**Windows:**
1. Apri Esplora Risorse (tasto Windows + E)
2. Vai dove hai estratto/creato la cartella del progetto
3. Fai click destro sulla cartella del progetto
4. Seleziona "Apri nel terminale" o "Apri finestra PowerShell qui"
   - Se non vedi questa opzione, vai al Passo 5b

**Passo 5b (se non hai "Apri nel terminale"):**
1. Apri il Prompt dei comandi (tasto Windows, scrivi `cmd`)
2. Scrivi `cd ` (cd con uno spazio)
3. Trascina la cartella del progetto nella finestra del prompt
4. Premi Invio

**Mac:**
1. Apri Finder
2. Vai dove hai estratto/creato la cartella del progetto
3. Fai click destro sulla cartella
4. Tieni premuto "Option" (Alt) e clicca "Copia percorso"
5. Apri Terminale
6. Scrivi `cd ` (cd con uno spazio)
7. Premi Cmd+V per incollare il percorso
8. Premi Invio

---

#### 🔹 Passo 6: Esegui lo script di installazione

⚠️ **IMPORTANTE:** Assicurati di essere nella cartella del progetto (vedi Passo 5)

**Windows:**
1. Nel Prompt dei comandi, scrivi:
   ```cmd
   setup.bat
   ```
2. Premi Invio
3. Aspetta che finisca (può richiedere 2-5 minuti)
4. Lo script installerà tutto automaticamente
5. Quando vedi "Setup completato con successo!", sei pronto

**Mac:**
1. Nel Terminale, scrivi:
   ```bash
   chmod +x setup.sh
   ```
2. Premi Invio
3. Poi scrivi:
   ```bash
   ./setup.sh
   ```
4. Premi Invio
5. Aspetta che finisca (può richiedere 2-5 minuti)
6. Quando vedi "Setup completato con successo!", sei pronto

---

### PARTE 4: AVVIA IL SISTEMA

#### 🔹 Passo 7: Avvia MongoDB (se non è già avviato)

**Windows:**
- MongoDB dovrebbe essere già avviato come servizio
- Se hai problemi, apri il Prompt dei comandi come Amministratore:
  1. Tasto Windows, scrivi `cmd`
  2. Fai click destro su "Prompt dei comandi"
  3. Clicca "Esegui come amministratore"
  4. Scrivi: `net start MongoDB`
  5. Premi Invio

**Mac:**
1. Apri un NUOVO Terminale
2. Scrivi:
   ```bash
   brew services start mongodb-community
   ```
3. Premi Invio

---

#### 🔹 Passo 8: Avvia il sistema Karaoke

**Windows:**
1. Vai nella cartella del progetto (Esplora Risorse)
2. Fai doppio click su `start-all.bat`
3. Si apriranno due finestre:
   - Una nera (Backend)
   - Una che poi aprirà il browser (Frontend)
4. Aspetta 10-20 secondi
5. Il browser si aprirà automaticamente su http://localhost:3000

**Mac:**
1. Apri Terminale
2. Vai nella cartella del progetto (vedi Passo 5)
3. Scrivi:
   ```bash
   ./start-all.sh
   ```
4. Premi Invio
5. Aspetta 10-20 secondi
6. Il browser si aprirà automaticamente su http://localhost:3000

---

### PARTE 5: USA IL SISTEMA

#### 🔹 Passo 9: Testa la pagina pubblica

1. Il browser dovrebbe aprirsi automaticamente
2. Se non si apre, vai manualmente su: **http://localhost:3000**
3. Vedrai il form di prenotazione
4. Prova a prenotare una canzone:
   - Nome: Mario
   - Canzone: Volare
   - Tonalità: Do
5. Clicca "Invia Prenotazione"
6. Ti verrà dato un codice (es: 001)
7. ✅ Ricorda questo codice!

---

#### 🔹 Passo 10: Accedi alla Dashboard Admin

1. Nel browser, vai su: **http://localhost:3000/admin/login**
2. Inserisci:
   - Username: `admin`
   - Password: `admin123`
3. Clicca "Accedi"
4. Vedrai la dashboard con:
   - Statistiche in alto
   - Lista cantanti con le loro canzoni
5. Prova a:
   - Cliccare ✓ verde per marcare una canzone come cantata
   - Cliccare 🗑️ rosso per eliminare
   - Usare lo switch per chiudere le prenotazioni

---

#### 🔹 Passo 11: Vedi la documentazione API (opzionale)

1. Nel browser, vai su: **http://localhost:8001/docs**
2. Vedrai tutte le API disponibili
3. Puoi testarle direttamente da lì

---

### 🛑 COME FERMARE IL SISTEMA

**Windows:**
1. Vai alla finestra nera del Backend
2. Premi `Ctrl+C`
3. Chiudi la finestra
4. Vai alla finestra del Frontend
5. Premi `Ctrl+C`
6. Chiudi la finestra

**Mac:**
1. Vai al Terminale
2. Premi `Ctrl+C`
3. Chiudi il Terminale

---

### 🔄 COME RIAVVIARE IL SISTEMA

Ogni volta che vuoi usare il sistema:

**Windows:**
1. Vai nella cartella del progetto
2. Doppio click su `start-all.bat`
3. Aspetta che si apra il browser

**Mac:**
1. Apri Terminale
2. Vai nella cartella del progetto: `cd /percorso/cartella`
3. Scrivi: `./start-all.sh`
4. Premi Invio

---

## ❓ PROBLEMI COMUNI

### "Python non è riconosciuto"
- Reinstalla Python e assicurati di spuntare "Add Python to PATH"
- Chiudi e riapri il Terminale/Prompt

### "Node non è riconosciuto"
- Reinstalla Node.js
- Chiudi e riapri il Terminale/Prompt

### "MongoDB non si avvia"
**Windows:**
- Vai a Servizi (tasto Windows, scrivi "services.msc")
- Cerca "MongoDB"
- Click destro → Avvia

**Mac:**
```bash
brew services start mongodb-community
```

### "La porta 3000 è già in uso"
- Qualche altro programma sta usando quella porta
- Chiudi tutti i programmi e riprova
- Oppure cambia porta nel file

### "Errore durante l'installazione"
- Assicurati di avere una connessione internet
- Prova a eseguire di nuovo lo script di setup
- Assicurati di essere amministratore (Windows) o usa `sudo` (Mac)

---

## 🌐 ACCESSO AL SISTEMA

Dopo aver avviato il sistema (vedi Passo 8 sopra):

### 📱 Pagina Pubblica (per i clienti)
**URL:** http://localhost:3000

Questa è la pagina che i tuoi clienti vedranno quando scansionano il QR code.

### 👨‍💼 Dashboard Amministratore
**URL:** http://localhost:3000/admin/login

**Credenziali di accesso:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANTE:** Quando usi il sistema per davvero, cambia questa password!

### 📚 Documentazione API
**URL:** http://localhost:8001/docs

Qui puoi vedere e testare tutte le API del sistema.

---

## 🎨 COME CREARE IL QR CODE PER I CLIENTI

Quando usi il sistema sul tuo PC locale:

1. Vai su un sito di generazione QR code gratuito:
   - https://www.qr-code-generator.com/
   - https://www.qrcode-monkey.com/
   
2. Inserisci l'URL: `http://TUO-IP-LOCALE:3000`
   
   **Per trovare il tuo IP locale:**
   - **Windows:** 
     1. Apri Prompt comandi
     2. Scrivi: `ipconfig`
     3. Cerca "Indirizzo IPv4" (es: 192.168.1.100)
   - **Mac:**
     1. Vai in Preferenze di Sistema
     2. Clicca Rete
     3. Vedi l'IP a destra

3. Genera il QR code

4. Scaricalo e stampalo

5. I clienti scannerizzeranno il QR code con il loro telefono

⚠️ **IMPORTANTE:** Il telefono dei clienti deve essere sulla STESSA rete WiFi del tuo PC!

---

## 💡 SUGGERIMENTI PER L'USO

### Per il Karaoke
1. Stampa il QR code e mettilo in un posto visibile
2. Tieni aperta la dashboard admin sul tuo PC
3. I clienti scannerizzano e prenotano
4. Tu vedi le prenotazioni in tempo reale
5. Marchi come "cantata" dopo ogni esibizione

### Organizzazione Turni
Il sistema NON segue l'ordine di arrivo delle prenotazioni.
Il numero #1, #2, #3 accanto a ogni canzone indica solo l'ordine in cui sono state prenotate.

**Come funziona meglio:**
- Fai cantare una canzone a ogni cantante
- Poi ricominci il giro
- Esempio: Mario canta la sua #1, poi Luca la sua #1, poi Sara la sua #1, poi Mario la sua #2...

---

## 🔧 INFORMAZIONI TECNICHE

### Stack Tecnologico

**Backend:**
- FastAPI - Framework API REST
- MongoDB - Database NoSQL
- Motor - Driver MongoDB asincrono
- PyJWT - Autenticazione JWT
- Bcrypt - Hashing password

**Frontend:**
- React 19 - UI library
- React Router - Navigazione
- Axios - HTTP client
- Tailwind CSS - Framework CSS
- Shadcn/UI - Componenti UI
- Sonner - Notifiche toast

### Struttura Database MongoDB

**Collection: singers**
```json
{
  "id": "uuid",
  "nome": "Mario",
  "codice": "001",
  "timestamp": "2025-01-13T10:30:00Z"
}
```

**Collection: songs**
```json
{
  "id": "uuid",
  "singer_id": "uuid-del-cantante",
  "canzone": "Volare",
  "tonalita": "Do",
  "ordine_prenotazione": 1,
  "cantata": false,
  "timestamp": "2025-01-13T10:30:00Z"
}
```

**Collection: settings**
```json
{
  "prenotazioni_aperte": true
}
```

**Collection: admins**
```json
{
  "username": "admin",
  "password": "hash-bcrypt"
}
```

---

## 📁 STRUTTURA FILE DEL PROGETTO

Ecco come sono organizzati i file:

```
karaoke/                          ← Cartella principale
│
├── backend/                      ← Tutto il codice del server
│   ├── server.py                 ← File principale API
│   ├── requirements.txt          ← Lista librerie Python
│   ├── .env                      ← Configurazione (URL database, ecc)
│   └── venv/                     ← Ambiente virtuale Python (creato automaticamente)
│
├── frontend/                     ← Tutto il codice dell'interfaccia
│   ├── src/
│   │   ├── pages/
│   │   │   ├── BookingPage.jsx       ← Pagina prenotazione pubblica
│   │   │   ├── AdminLogin.jsx        ← Pagina login admin
│   │   │   └── AdminDashboard.jsx    ← Dashboard amministratore
│   │   ├── components/ui/            ← Componenti interfaccia (bottoni, card, ecc)
│   │   ├── App.js                    ← File principale React
│   │   └── App.css                   ← Stili globali
│   ├── package.json              ← Lista librerie Node.js
│   ├── .env                      ← Configurazione frontend
│   └── node_modules/             ← Librerie (creato automaticamente)
│
├── setup.sh                      ← Script installazione Mac/Linux
├── setup.bat                     ← Script installazione Windows
├── start-all.sh                  ← Script avvio completo Mac/Linux
├── start-all.bat                 ← Script avvio completo Windows
├── start-backend.sh              ← Avvia solo backend Mac/Linux
├── start-backend.bat             ← Avvia solo backend Windows
├── start-frontend.sh             ← Avvia solo frontend Mac/Linux
├── start-frontend.bat            ← Avvia solo frontend Windows
└── README.md                     ← Questo file (documentazione)
```

---

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
