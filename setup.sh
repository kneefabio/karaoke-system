#!/bin/bash

# Script di installazione automatica - Sistema Prenotazioni Karaoke
# Per Mac/Linux

echo "================================="
echo "Setup Sistema Prenotazioni Karaoke"
echo "================================="
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica prerequisiti
echo "${YELLOW}[1/6] Verifica prerequisiti...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "${RED}✗ Python 3 non trovato. Installa Python 3.11+ da https://www.python.org/${NC}"
    exit 1
fi
echo "${GREEN}✓ Python 3 trovato${NC}"

if ! command -v node &> /dev/null; then
    echo "${RED}✗ Node.js non trovato. Installa Node.js 18+ da https://nodejs.org/${NC}"
    exit 1
fi
echo "${GREEN}✓ Node.js trovato${NC}"

if ! command -v mongod &> /dev/null; then
    echo "${YELLOW}⚠ MongoDB non trovato. Installa MongoDB da https://www.mongodb.com/try/download/community${NC}"
    echo "Continuo comunque, ma dovrai avviare MongoDB manualmente."
else
    echo "${GREEN}✓ MongoDB trovato${NC}"
fi

if ! command -v yarn &> /dev/null; then
    echo "${YELLOW}⚠ Yarn non trovato. Installo Yarn...${NC}"
    npm install -g yarn
fi
echo "${GREEN}✓ Yarn pronto${NC}"

echo ""

# Setup Backend
echo "${YELLOW}[2/6] Configurazione Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creazione ambiente virtuale Python..."
    python3 -m venv venv
fi

echo "Attivazione ambiente virtuale..."
source venv/bin/activate

echo "Installazione dipendenze Python..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "Configurazione file .env per ambiente locale..."
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=karaoke_db
CORS_ORIGINS=http://localhost:3000
JWT_SECRET=karaoke_secret_key_change_in_production
EOF

echo "${GREEN}✓ Backend configurato${NC}"
cd ..
echo ""

# Setup Frontend
echo "${YELLOW}[3/6] Configurazione Frontend...${NC}"
cd frontend

echo "Installazione dipendenze Node.js..."
yarn install --silent

echo "Configurazione file .env per ambiente locale..."
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
EOF

echo "${GREEN}✓ Frontend configurato${NC}"
cd ..
echo ""

# Crea script di avvio
echo "${YELLOW}[4/6] Creazione script di avvio...${NC}"

cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "Avvio Backend su http://localhost:8001..."
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
EOF
chmod +x start-backend.sh

cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "Avvio Frontend su http://localhost:3000..."
cd frontend
yarn start
EOF
chmod +x start-frontend.sh

cat > start-all.sh << 'EOF'
#!/bin/bash
echo "================================="
echo "Avvio Sistema Karaoke"
echo "================================="
echo ""

# Verifica MongoDB
if ! pgrep -x "mongod" > /dev/null; then
    echo "Avvio MongoDB..."
    mongod --fork --logpath /tmp/mongodb.log --dbpath ~/data/db 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✓ MongoDB avviato"
    else
        echo "⚠ Avvia MongoDB manualmente in un altro terminale: mongod"
    fi
else
    echo "✓ MongoDB già in esecuzione"
fi

echo ""
echo "Avvio Backend e Frontend..."
echo ""
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8001/docs"
echo ""
echo "Login Admin: username=admin, password=admin123"
echo ""
echo "Premi Ctrl+C per fermare tutti i servizi"
echo ""

# Avvia backend in background
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001 > /tmp/karaoke-backend.log 2>&1 &
BACKEND_PID=$!
cd ..

sleep 3

# Avvia frontend
cd frontend
yarn start

# Cleanup quando si ferma
trap "kill $BACKEND_PID 2>/dev/null" EXIT
EOF
chmod +x start-all.sh

echo "${GREEN}✓ Script di avvio creati${NC}"
echo ""

# Crea directory MongoDB se non esiste
echo "${YELLOW}[5/6] Preparazione directory MongoDB...${NC}"
mkdir -p ~/data/db
echo "${GREEN}✓ Directory MongoDB pronta${NC}"
echo ""

# Riepilogo
echo "${GREEN}[6/6] ================================="
echo "Setup completato con successo!"
echo "=================================${NC}"
echo ""
echo "${YELLOW}Per avviare il sistema:${NC}"
echo "  ./start-all.sh        - Avvia tutto automaticamente"
echo ""
echo "${YELLOW}Oppure avvia separatamente:${NC}"
echo "  ./start-backend.sh    - Solo backend"
echo "  ./start-frontend.sh   - Solo frontend"
echo ""
echo "${YELLOW}Accesso:${NC}"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8001"
echo "  API Docs:  http://localhost:8001/docs"
echo ""
echo "${YELLOW}Credenziali Admin:${NC}"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "${GREEN}Buon divertimento con il tuo sistema Karaoke! 🎤${NC}"
