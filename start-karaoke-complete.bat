@echo off
chcp 65001 >nul
title Sistema Karaoke - Avvio Completo

cls
echo.
echo ========================================
echo   SISTEMA KARAOKE - AVVIO COMPLETO
echo ========================================
echo.
echo Questo script avvia:
echo 1. Backend (FastAPI + MongoDB)
echo 2. Frontend (React)
echo 3. Photo Overlay (Electron)
echo.
echo Premi un tasto per iniziare...
pause >nul

REM Verifica prerequisiti
set "PROJECT_DIR=%CD%"

echo.
echo [1/5] Verifica MongoDB...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] MongoDB in esecuzione
) else (
    echo [ATTENZIONE] MongoDB non in esecuzione!
    echo Avvio MongoDB come servizio...
    net start MongoDB 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo [ERRORE] Impossibile avviare MongoDB
        echo Avvialo manualmente: mongod
        echo.
        pause
    )
)

echo.
echo [2/5] Avvio Backend...
start "Karaoke Backend" cmd /k "cd /d "%PROJECT_DIR%\backend" && call venv\Scripts\activate.bat && echo Backend avviato su http://localhost:8001 && uvicorn server:app --reload --host 0.0.0.0 --port 8001"

echo Attendo 5 secondi per l'avvio del backend...
timeout /t 5 /nobreak >nul

echo.
echo [3/5] Avvio Frontend...
start "Karaoke Frontend" cmd /k "cd /d "%PROJECT_DIR%\frontend" && echo Frontend avviato su http://localhost:3000 && yarn start"

echo Attendo 3 secondi...
timeout /t 3 /nobreak >nul

echo.
echo [4/5] Avvio Photo Overlay...
if exist "%PROJECT_DIR%\electron-overlay\node_modules" (
    start "Karaoke Overlay" cmd /k "cd /d "%PROJECT_DIR%\electron-overlay" && echo Photo Overlay attivo && npm start"
) else (
    echo [ATTENZIONE] Overlay non installato. Installo dipendenze...
    start "Karaoke Overlay" cmd /k "cd /d "%PROJECT_DIR%\electron-overlay" && npm install && echo Overlay pronto! && npm start"
)

echo.
echo [5/5] ========================================
echo    SISTEMA AVVIATO!
echo ========================================
echo.
echo Finestre aperte:
echo   1. Backend  - http://localhost:8001
echo   2. Frontend - http://localhost:3000  
echo   3. Overlay  - Finestra trasparente
echo.
echo ========================================
echo   ACCESSI:
echo ========================================
echo.
echo Pagina Pubblica:
echo   http://localhost:3000
echo.
echo Dashboard Admin:
echo   http://localhost:3000/admin/login
echo   Username: admin
echo   Password: admin123
echo.
echo Super Admin (Gestione Licenze):
echo   http://localhost:3000/super-admin
echo   Username: superadmin
echo   Password: superadmin123
echo.
echo Gestione Serate Foto:
echo   http://localhost:3000/admin/serate
echo.
echo API Docs:
echo   http://localhost:8001/docs
echo.
echo ========================================
echo   OVERLAY CONTROLLI:
echo ========================================
echo.
echo Nella finestra Overlay:
echo   - Premi C per configurazione
echo   - Premi T per test
echo   - Premi Q per uscire
echo.
echo ========================================
echo.
echo Per fermare tutto:
echo - Chiudi le 3 finestre (Ctrl+C in ognuna)
echo - Oppure chiudi questa finestra
echo.
echo Il browser si aprirà automaticamente...
echo.
pause

REM Apri browser
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo Sistema pronto! Buon karaoke! 🎤
echo.
