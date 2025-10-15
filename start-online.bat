@echo off
chcp 65001 >nul
title Karaoke Online con ngrok

cls
echo.
echo ========================================
echo   SISTEMA KARAOKE - MODALITA ONLINE
echo ========================================
echo.
echo IMPORTANTE: Prima di usare questo script:
echo 1. Esegui "build-for-online.bat" (una volta sola)
echo 2. Poi usa questo script per avviare
echo.
pause

REM Verifica build frontend
if not exist "frontend\build\index.html" (
    echo.
    echo [ERRORE] Build frontend non trovato!
    echo.
    echo Devi prima buildare il frontend:
    echo 1. Doppio click su: build-for-online.bat
    echo 2. Aspetta che finisca
    echo 3. Poi rilancia questo script
    echo.
    pause
    exit /b 1
)

REM Verifica ngrok
if not exist "C:\ngrok\ngrok.exe" (
    echo.
    echo [ERRORE] ngrok non trovato!
    echo.
    echo Installa ngrok:
    echo 1. Vai su https://ngrok.com/download
    echo 2. Scarica ed estrai in C:\ngrok
    echo 3. Registrati e configura il token:
    echo    cd C:\ngrok
    echo    ngrok config add-authtoken TUO_TOKEN
    echo.
    pause
    exit /b 1
)

echo.
echo [1/2] Avvio Backend (serve anche frontend)...
echo.

set "PROJECT_DIR=%CD%"

REM Verifica che la cartella backend esista
if not exist "%PROJECT_DIR%\backend" (
    echo [ERRORE] Cartella backend non trovata!
    echo Sei nella cartella del progetto?
    pause
    exit /b 1
)

echo Avvio backend...
REM Avvia backend (SENZA --reload per produzione)
start "Karaoke Server" cmd /k "cd /d "%PROJECT_DIR%\backend" && call venv\Scripts\activate.bat && echo Server avviato su porta 8001 && uvicorn server:app --host 0.0.0.0 --port 8001"

echo Backend avviato nella finestra separata
echo.
echo Attendo 10 secondi...
timeout /t 10 /nobreak >nul

echo.
echo [2/2] Avvio ngrok...
echo.

REM Avvia ngrok
start "ngrok - Karaoke" cmd /k "cd C:\ngrok && ngrok http 8001"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   SISTEMA ONLINE - ISTRUZIONI
echo ========================================
echo.
echo SONO STATE APERTE 2 FINESTRE:
echo.
echo 1. Backend+Frontend - Server completo (NON chiudere)
echo 2. ngrok - Tunnel Internet (GUARDA QUESTA!)
echo.
echo ========================================
echo   PROSSIMI PASSI:
echo ========================================
echo.
echo PASSO 1: Guarda la finestra "ngrok"
echo          Troverai una riga tipo:
echo          Forwarding: https://abc123.ngrok-free.app
echo.
echo PASSO 2: COPIA quell'URL completo
echo.
echo PASSO 3: Genera QR Code
echo          - Vai su: https://www.qr-code-generator.com/
echo          - Incolla l'URL di ngrok
echo          - Genera e stampa il QR
echo.
echo PASSO 4: TESTA dal tuo smartphone
echo          - Scannerizza il QR
echo          - Dovresti vedere il form di prenotazione
echo.
echo PASSO 5: Dashboard Admin
echo          - Stesso URL di ngrok + /admin/login
echo          - Es: https://abc123.ngrok-free.app/admin/login
echo          - User: admin / Pass: admin123
echo.
echo ========================================
echo   IMPORTANTE:
echo ========================================
echo.
echo - Ora TUTTO passa attraverso la porta 8001
echo - Un solo URL per frontend E backend
echo - NON serve piu avviare il frontend separatamente
echo - L'URL ngrok cambia ogni riavvio (piano gratuito)
echo.
echo ========================================
echo.
echo Per fermare tutto:
echo - Premi Ctrl+C in ENTRAMBE le finestre
echo.
pause
