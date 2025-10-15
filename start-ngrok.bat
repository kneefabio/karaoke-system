@echo off
chcp 65001 >nul
title Avvio ngrok

echo ========================================
echo   AVVIO NGROK
echo ========================================
echo.

if not exist "C:\ngrok\ngrok.exe" (
    echo [ERRORE] ngrok non trovato in C:\ngrok
    echo.
    echo Installalo da: https://ngrok.com/download
    echo.
    pause
    exit /b 1
)

cd C:\ngrok

echo Avvio ngrok sulla porta 8001...
echo.
echo IMPORTANTE: Copia l'URL che appare sotto!
echo Es: https://abc123.ngrok-free.app
echo.

ngrok http 8001
