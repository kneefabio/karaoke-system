@echo off
echo ========================================
echo   Karaoke Photo Overlay - Avvio
echo ========================================
echo.
echo Avvio dell'overlay in corso...
echo.
echo NOTA: Se ricevi errori, usa 'install-and-start.bat'
echo       per installare prima le dipendenze.
echo.

cd /d "%~dp0"
call yarn start

pause
