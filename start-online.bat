@echo off
chcp 65001 >nul
title Karaoke Online con ngrok

cls
echo.
echo ========================================
echo   SISTEMA KARAOKE - MODALITA ONLINE
echo ========================================
echo.
echo Questo script avviera:
echo 1. Backend (server locale)
echo 2. Frontend (interfaccia)
echo 3. ngrok (esposizione a Internet)
echo.
echo PREREQUISITO: ngrok installato in C:\ngrok
echo.
pause

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
echo [1/3] Avvio Backend e Frontend...
echo.

REM Salva directory corrente
set "PROJECT_DIR=%CD%"

REM Avvia backend
start "Karaoke Backend" cmd /k "cd /d "%PROJECT_DIR%\backend" && venv\Scripts\activate.bat && uvicorn server:app --reload --host 0.0.0.0 --port 8001"

echo Backend avviato in finestra separata
echo.
echo Attendo 8 secondi per l'avvio...
timeout /t 8 /nobreak >nul

REM Avvia frontend
start "Karaoke Frontend" cmd /k "cd /d "%PROJECT_DIR%\frontend" && yarn start"

echo Frontend avviato in finestra separata
echo.
echo Attendo altri 5 secondi...
timeout /t 5 /nobreak >nul

echo.
echo [2/3] Avvio ngrok...
echo.

REM Avvia ngrok
start "ngrok - Karaoke" cmd /k "cd C:\ngrok && ngrok http 8001"

echo.
echo ========================================
echo [3/3] SISTEMA ONLINE - ISTRUZIONI
echo ========================================
echo.
echo SONO STATE APERTE 3 FINESTRE:
echo.
echo 1. Backend  - Server locale (NON chiudere)
echo 2. Frontend - Interfaccia web (NON chiudere)
echo 3. ngrok    - Tunnel Internet (GUARDA QUESTA!)
echo.
echo ========================================
echo   PROSSIMI PASSI:
echo ========================================
echo.
echo PASSO 1: Guarda la finestra "ngrok"
echo          Troverai una riga tipo:
echo          Forwarding: https://abc123.ngrok-free.app
echo.
echo PASSO 2: COPIA quell'URL (https://...)
echo.
echo PASSO 3: Genera QR Code
echo          - Vai su: https://www.qr-code-generator.com/
echo          - Incolla l'URL di ngrok
echo          - Genera e stampa il QR
echo.
echo PASSO 4: Dashboard Admin (sul tuo PC)
echo          - Browser: http://localhost:3000/admin/login
echo          - User: admin
echo          - Pass: admin123
echo.
echo PASSO 5: Gli ospiti scannerizzano il QR
echo          Vedranno la pagina di prenotazione!
echo.
echo ========================================
echo   IMPORTANTE:
echo ========================================
echo.
echo - NON chiudere le 3 finestre durante la serata
echo - L'URL di ngrok cambia ogni volta (piano gratuito)
echo - Per URL fisso: ngrok Pro ($8/mese)
echo.
echo ========================================
echo.
echo Per fermare tutto:
echo - Premi Ctrl+C in TUTTE le finestre
echo - Oppure chiudi le finestre
echo.
pause
