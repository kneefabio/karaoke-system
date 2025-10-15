@echo off
chcp 65001 >nul
title Avvio Backend per Online

echo ========================================
echo   AVVIO BACKEND (con Frontend incluso)
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat

echo.
echo Avvio server su porta 8001...
echo Il server serve sia backend che frontend.
echo.
echo URL locale: http://localhost:8001
echo.
echo Per accesso remoto, avvia ngrok in un altro terminale:
echo   cd C:\ngrok
echo   ngrok http 8001
echo.
echo Premi Ctrl+C per fermare
echo.

uvicorn server:app --host 0.0.0.0 --port 8001

pause
