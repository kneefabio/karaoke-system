@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

echo =================================
echo Setup Sistema Prenotazioni Karaoke
echo =================================
echo.

REM Verifica prerequisiti
echo [1/6] Verifica prerequisiti...

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Python non trovato. Installa Python 3.11+ da https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python trovato

where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Node.js non trovato. Installa Node.js 18+ da https://nodejs.org/
    pause
    exit /b 1
)
echo ✓ Node.js trovato

where mongod >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠ MongoDB non trovato. Installa MongoDB da https://www.mongodb.com/try/download/community
    echo Continuo comunque, ma dovrai avviare MongoDB manualmente.
) else (
    echo ✓ MongoDB trovato
)

where yarn >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠ Yarn non trovato. Installo Yarn...
    call npm install -g yarn
)
echo ✓ Yarn pronto
echo.

REM Setup Backend
echo [2/6] Configurazione Backend...
cd backend

if not exist "venv" (
    echo Creazione ambiente virtuale Python...
    python -m venv venv
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo Installazione dipendenze Python...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo Configurazione file .env per ambiente locale...
(
    echo MONGO_URL=mongodb://localhost:27017
    echo DB_NAME=karaoke_db
    echo CORS_ORIGINS=http://localhost:3000
    echo JWT_SECRET=karaoke_secret_key_change_in_production
) > .env

echo ✓ Backend configurato
cd ..
echo.

REM Setup Frontend
echo [3/6] Configurazione Frontend...
cd frontend

echo Installazione dipendenze Node.js...
call yarn install --silent

echo Configurazione file .env per ambiente locale...
(
    echo REACT_APP_BACKEND_URL=http://localhost:8001
) > .env

echo ✓ Frontend configurato
cd ..
echo.

REM Crea script di avvio
echo [4/6] Creazione script di avvio...

REM Script backend
(
    echo @echo off
    echo echo Avvio Backend su http://localhost:8001...
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo uvicorn server:app --reload --host 0.0.0.0 --port 8001
) > start-backend.bat

REM Script frontend
(
    echo @echo off
    echo echo Avvio Frontend su http://localhost:3000...
    echo cd frontend
    echo yarn start
) > start-frontend.bat

REM Script completo
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo echo =================================
    echo echo Avvio Sistema Karaoke
    echo echo =================================
    echo echo.
    echo.
    echo echo Verifica MongoDB...
    echo tasklist /FI "IMAGENAME eq mongod.exe" 2^>NUL ^| find /I /N "mongod.exe"^>NUL
    echo if "%%ERRORLEVEL%%"=="0" (
    echo     echo ✓ MongoDB già in esecuzione
    echo ^) else (
    echo     echo ⚠ Avvia MongoDB manualmente in un altro terminale: mongod
    echo     echo    oppure come servizio Windows
    echo ^
    echo.
    echo echo.
    echo echo Backend: http://localhost:8001
    echo echo Frontend: http://localhost:3000
    echo echo API Docs: http://localhost:8001/docs
    echo echo.
    echo echo Login Admin: username=admin, password=admin123
    echo echo.
    echo echo Premi Ctrl+C per fermare i servizi
    echo echo.
    echo.
    echo REM Avvia backend in una nuova finestra
    echo start "Karaoke Backend" cmd /k "cd backend ^&^& venv\Scripts\activate.bat ^&^& uvicorn server:app --reload --host 0.0.0.0 --port 8001"
    echo.
    echo timeout /t 3 /nobreak ^>nul
    echo.
    echo REM Avvia frontend
    echo cd frontend
    echo yarn start
) > start-all.bat

echo ✓ Script di avvio creati
echo.

REM Crea directory MongoDB
echo [5/6] Preparazione directory MongoDB...
if not exist "%USERPROFILE%\data\db" (
    mkdir "%USERPROFILE%\data\db"
)
echo ✓ Directory MongoDB pronta
echo.

REM Riepilogo
echo [6/6] =================================
echo Setup completato con successo!
echo =================================
echo.
echo Per avviare il sistema:
echo   start-all.bat         - Avvia tutto automaticamente
echo.
echo Oppure avvia separatamente:
echo   start-backend.bat     - Solo backend
echo   start-frontend.bat    - Solo frontend
echo.
echo Accesso:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8001
echo   API Docs:  http://localhost:8001/docs
echo.
echo Credenziali Admin:
echo   Username: admin
echo   Password: admin123
echo.
echo Buon divertimento con il tuo sistema Karaoke! 🎤
echo.
pause
