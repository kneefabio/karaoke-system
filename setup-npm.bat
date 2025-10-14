@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

title Setup Sistema Karaoke (versione NPM)

echo ========================================
echo   SETUP SISTEMA PRENOTAZIONI KARAOKE
echo   Versione NPM (senza Yarn)
echo ========================================
echo.
echo Questo processo richiede 2-5 minuti.
echo.
pause

REM Verifica prerequisiti
echo.
echo [1/5] Verifica prerequisiti...
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Python non trovato!
    echo.
    echo Devi installare Python prima di continuare:
    echo 1. Vai su https://www.python.org/downloads/release/python-3119/
    echo 2. Scarica "Windows installer (64-bit)"
    echo 3. IMPORTANTE: Spunta "Add Python to PATH" durante installazione
    echo 4. Riavvia questo script
    echo.
    pause
    exit /b 1
)
echo [OK] Python trovato

where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Node.js non trovato!
    echo.
    echo Devi installare Node.js prima di continuare:
    echo 1. Vai su https://nodejs.org/
    echo 2. Scarica la versione LTS
    echo 3. Installa seguendo le istruzioni
    echo 4. Riavvia questo script
    echo.
    pause
    exit /b 1
)
echo [OK] Node.js trovato

where mongod >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ATTENZIONE] MongoDB non trovato nel PATH!
    echo.
    echo Se il servizio MongoDB e' gia avviato, puoi continuare.
    echo Altrimenti installa MongoDB da:
    echo https://www.mongodb.com/try/download/community
    echo.
    echo Premi un tasto per continuare comunque...
    pause >nul
) else (
    echo [OK] MongoDB trovato
)

echo.
echo [OK] Tutti i prerequisiti verificati
echo.

REM Setup Backend
echo.
echo [2/5] Configurazione Backend...
echo.
if not exist "backend" (
    echo [ERRORE] Cartella backend non trovata!
    echo Assicurati di essere nella cartella principale del progetto.
    pause
    exit /b 1
)

cd backend

if not exist "venv" (
    echo Creazione ambiente virtuale Python...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRORE] Impossibile creare ambiente virtuale
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtuale creato
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Impossibile attivare ambiente virtuale
    cd ..
    pause
    exit /b 1
)

echo Installazione dipendenze Python...
echo (questo puo richiedere 2-3 minuti, attendi...)
echo.
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Installazione dipendenze fallita
    echo.
    echo Possibili cause:
    echo - Hai Python 3.14? Installa Python 3.11 invece
    echo - Manca un compilatore C++? Vedi README per dettagli
    echo.
    cd ..
    pause
    exit /b 1
)

echo.
echo [OK] Dipendenze Python installate

echo Configurazione file .env per ambiente locale...
(
    echo MONGO_URL=mongodb://localhost:27017
    echo DB_NAME=karaoke_db
    echo CORS_ORIGINS=http://localhost:3000
    echo JWT_SECRET=karaoke_secret_key_change_in_production
) > .env

echo [OK] Backend configurato
cd ..
echo.

REM Setup Frontend
echo.
echo [3/5] Configurazione Frontend...
echo.
if not exist "frontend" (
    echo [ERRORE] Cartella frontend non trovata!
    echo Assicurati di essere nella cartella principale del progetto.
    pause
    exit /b 1
)

cd frontend

echo Installazione dipendenze Node.js con NPM...
echo (questo puo richiedere 3-5 minuti, attendi...)
echo.
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Installazione dipendenze fallita
    echo Controlla la connessione internet e riprova
    echo.
    cd ..
    pause
    exit /b 1
)

echo.
echo [OK] Dipendenze Node.js installate

echo Configurazione file .env per ambiente locale...
(
    echo REACT_APP_BACKEND_URL=http://localhost:8001
) > .env

echo [OK] Frontend configurato
cd ..
echo.

REM Crea script di avvio
echo.
echo [4/5] Creazione script di avvio...
echo.

REM Script backend
(
    echo @echo off
    echo title Karaoke Backend
    echo echo ========================================
    echo echo Avvio Backend su http://localhost:8001
    echo echo ========================================
    echo echo.
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo echo Backend in esecuzione...
    echo echo Documentazione API: http://localhost:8001/docs
    echo echo.
    echo echo Premi Ctrl+C per fermare
    echo echo.
    echo uvicorn server:app --reload --host 0.0.0.0 --port 8001
    echo pause
) > start-backend.bat

REM Script frontend
(
    echo @echo off
    echo title Karaoke Frontend
    echo echo ========================================
    echo echo Avvio Frontend su http://localhost:3000
    echo echo ========================================
    echo echo.
    echo cd frontend
    echo echo Frontend in esecuzione...
    echo echo Il browser si aprira automaticamente
    echo echo.
    echo echo Premi Ctrl+C per fermare
    echo echo.
    echo npm start
    echo pause
) > start-frontend.bat

REM Script completo
(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Sistema Karaoke
    echo cls
    echo.
    echo ========================================
    echo   SISTEMA PRENOTAZIONI KARAOKE
    echo ========================================
    echo.
    echo Controllo MongoDB...
    echo.
    echo tasklist /FI "IMAGENAME eq mongod.exe" 2^>NUL ^| find /I /N "mongod.exe"^>NUL
    echo if "%%ERRORLEVEL%%"=="0" (
    echo     echo [OK] MongoDB in esecuzione
    echo ^) else (
    echo     echo [ATTENZIONE] MongoDB non in esecuzione!
    echo     echo.
    echo     echo Avvia MongoDB prima di continuare:
    echo     echo - Apri un nuovo Prompt come Amministratore
    echo     echo - Scrivi: net start MongoDB
    echo     echo.
    echo     echo Oppure avvia mongod manualmente
    echo     echo.
    echo     pause
    echo ^)
    echo.
    echo ========================================
    echo   INFORMAZIONI ACCESSO
    echo ========================================
    echo.
    echo Pagina Pubblica:  http://localhost:3000
    echo Dashboard Admin:  http://localhost:3000/admin/login
    echo API Docs:         http://localhost:8001/docs
    echo.
    echo Credenziali Admin:
    echo   Username: admin
    echo   Password: admin123
    echo.
    echo ========================================
    echo.
    echo Il backend si aprira in una finestra separata
    echo Il frontend si aprira nel browser
    echo.
    echo Premi un tasto per avviare...
    echo pause ^>nul
    echo.
    echo echo Avvio Backend...
    echo start "Karaoke Backend" cmd /k "cd backend ^&^& venv\Scripts\activate.bat ^&^& uvicorn server:app --reload --host 0.0.0.0 --port 8001"
    echo.
    echo echo Attendo 5 secondi...
    echo timeout /t 5 /nobreak ^>nul
    echo.
    echo echo Avvio Frontend...
    echo cd frontend
    echo npm start
) > start-all.bat

echo [OK] Script di avvio creati:
echo   - start-all.bat      (avvia tutto)
echo   - start-backend.bat  (solo backend)
echo   - start-frontend.bat (solo frontend)
echo.

REM Crea directory MongoDB
echo.
echo [5/5] Preparazione directory MongoDB...
if not exist "%USERPROFILE%\data\db" (
    mkdir "%USERPROFILE%\data\db"
    echo [OK] Directory MongoDB creata
) else (
    echo [OK] Directory MongoDB gia esistente
)
echo.

REM Riepilogo
echo.
echo ========================================
echo    SETUP COMPLETATO CON SUCCESSO!
echo ========================================
echo.
echo Prossimi passi:
echo.
echo 1. Assicurati che MongoDB sia avviato
echo    Prompt Amministratore: net start MongoDB
echo.
echo 2. Per avviare il sistema, fai doppio click su:
echo    start-all.bat
echo.
echo 3. Accedi al sistema:
echo    - Pagina Pubblica:  http://localhost:3000
echo    - Dashboard Admin:  http://localhost:3000/admin/login
echo.
echo 4. Credenziali Admin:
echo    - Username: admin
echo    - Password: admin123
echo.
echo ========================================
echo.
echo NOTA: Questa versione usa NPM invece di Yarn
echo.
pause
