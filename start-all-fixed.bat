@echo off
chcp 65001 >nul
title Sistema Karaoke
cls
echo.
echo ========================================
echo   SISTEMA PRENOTAZIONI KARAOKE
echo ========================================
echo.
echo Controllo MongoDB...
echo.

tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MongoDB in esecuzione
) else (
    echo [ATTENZIONE] MongoDB non in esecuzione!
    echo.
    echo Avvia MongoDB prima di continuare:
    echo - Apri un nuovo Prompt come Amministratore
    echo - Scrivi: net start MongoDB
    echo.
    echo Oppure avvia mongod manualmente
    echo.
    pause
)

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
pause >nul
echo.

REM Salva la directory corrente
set "PROJECT_DIR=%CD%"

REM Verifica che le cartelle esistano
if not exist "%PROJECT_DIR%\backend" (
    echo [ERRORE] Cartella backend non trovata!
    echo Assicurati di eseguire questo file dalla cartella principale del progetto.
    pause
    exit /b 1
)

if not exist "%PROJECT_DIR%\frontend" (
    echo [ERRORE] Cartella frontend non trovata!
    echo Assicurati di eseguire questo file dalla cartella principale del progetto.
    pause
    exit /b 1
)

echo Avvio Backend...
start "Karaoke Backend" cmd /k "cd /d "%PROJECT_DIR%\backend" && venv\Scripts\activate.bat && uvicorn server:app --reload --host 0.0.0.0 --port 8001"

echo Attendo 5 secondi per l'avvio del backend...
timeout /t 5 /nobreak >nul
echo.

echo Avvio Frontend...
cd /d "%PROJECT_DIR%\frontend"
yarn start
