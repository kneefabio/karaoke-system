@echo off
chcp 65001 >nul
title Build e Deploy Sistema Karaoke

echo ========================================
echo   BUILD FRONTEND PER DEPLOY
echo ========================================
echo.
echo Questo script prepara il sistema per l'uso online.
echo Il frontend sara servito dal backend su porta 8001.
echo.
pause

set "PROJECT_DIR=%CD%"

REM Build Frontend
echo.
echo [1/2] Build del Frontend...
echo (questo puo richiedere 2-3 minuti)
echo.

cd frontend

REM Configura per build
echo Configurazione per produzione...
(
    echo REACT_APP_BACKEND_URL=/
) > .env.production

echo Building...
call yarn build
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Build fallito
    pause
    exit /b 1
)

echo [OK] Frontend buildato in frontend/build
cd ..

REM Riavvia Backend
echo.
echo [2/2] Il backend ora servira anche il frontend
echo.
echo Riavvia il backend per applicare le modifiche:
echo 1. Chiudi la finestra del backend (se aperta)
echo 2. Rilancia: start-backend.bat
echo.
echo ========================================
echo   BUILD COMPLETATO!
echo ========================================
echo.
echo Ora puoi usare UN SOLO URL per tutto:
echo.
echo CON NGROK:
echo   ngrok http 8001
echo   URL: https://abc123.ngrok-free.app
echo.
echo Questo URL serve sia il frontend che il backend!
echo.
echo ========================================
echo.
pause
