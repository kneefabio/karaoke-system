@echo off
chcp 65001 >nul
title Debug Avvio Online

echo ========================================
echo   DEBUG - Avvio Sistema Online
echo ========================================
echo.

set "PROJECT_DIR=%CD%"

echo Directory corrente: %PROJECT_DIR%
echo.

REM Verifica struttura
echo Verifica file e cartelle...
echo.

if exist "backend\server.py" (
    echo [OK] backend\server.py trovato
) else (
    echo [ERRORE] backend\server.py NON trovato!
)

if exist "backend\venv" (
    echo [OK] backend\venv trovato
) else (
    echo [ERRORE] backend\venv NON trovato! Esegui setup.bat
)

if exist "frontend\build\index.html" (
    echo [OK] frontend\build\index.html trovato
) else (
    echo [ERRORE] frontend\build NON trovato! Esegui build-for-online.bat
)

if exist "C:\ngrok\ngrok.exe" (
    echo [OK] ngrok trovato
) else (
    echo [ERRORE] ngrok NON trovato in C:\ngrok
)

echo.
echo ========================================
echo   Test Avvio Backend
echo ========================================
echo.
echo Provo ad avviare il backend...
echo Guarda la finestra che si apre per vedere errori.
echo.
pause

start "Test Backend" cmd /k "cd /d "%PROJECT_DIR%\backend" && call venv\Scripts\activate.bat && python --version && echo. && echo Provo ad avviare uvicorn... && echo. && uvicorn server:app --host 0.0.0.0 --port 8001"

echo.
echo Backend avviato in finestra separata.
echo.
echo Controlla quella finestra:
echo - Se vedi errori rossi, copia e mandali
echo - Se vedi "Uvicorn running on...", funziona!
echo.
echo ========================================
echo.
echo Dopo aver controllato, premi un tasto qui...
pause
echo.

REM Test ngrok
if exist "C:\ngrok\ngrok.exe" (
    echo.
    echo ========================================
    echo   Test ngrok
    echo ========================================
    echo.
    echo Provo ad avviare ngrok...
    echo.
    
    start "Test ngrok" cmd /k "cd C:\ngrok && ngrok http 8001"
    
    echo.
    echo ngrok avviato in finestra separata.
    echo.
    echo Controlla quella finestra:
    echo - Vedi "Forwarding https://..." ?
    echo - Copia quell'URL
    echo.
)

echo.
echo ========================================
echo   RISULTATI TEST
echo ========================================
echo.
echo Se entrambe le finestre sono aperte:
echo 1. Backend mostra "Uvicorn running"
echo 2. ngrok mostra "Forwarding"
echo.
echo Allora funziona tutto!
echo.
echo Se vedi errori, copiali e mandali.
echo.
pause
