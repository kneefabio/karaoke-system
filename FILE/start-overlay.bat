@echo off
title Karaoke Photo Overlay

echo ========================================
echo   KARAOKE PHOTO OVERLAY
echo ========================================
echo.
echo Avvio overlay foto in fullscreen...
echo.
echo CONTROLLI:
echo - Premi C per configurare
echo - Premi T per testare
echo - Premi Q per uscire
echo.

cd electron-overlay

if not exist "node_modules" (
    echo Installazione dipendenze...
    call npm install
)

echo.
echo Avvio app...
echo.

npm start
