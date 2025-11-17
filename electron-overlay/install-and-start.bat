@echo off
echo ========================================
echo   Karaoke Photo Overlay
echo   Installazione e Avvio
echo ========================================
echo.
echo Controllo Node.js...
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRORE: Node.js non trovato!
    echo.
    echo Scarica e installa Node.js da:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo Node.js trovato: OK
node --version
echo.

cd /d "%~dp0"

echo Installazione dipendenze...
echo Questo potrebbe richiedere 1-2 minuti...
echo.

call yarn install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRORE durante l'installazione!
    echo Prova con: npm install
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installazione completata!
echo ========================================
echo.
echo Avvio overlay...
echo.
echo COMANDI:
echo   C = Configurazione
echo   Q = Chiudi
echo.
echo RICORDA: Inserisci il tuo username admin nella configurazione!
echo.

call yarn start

pause
