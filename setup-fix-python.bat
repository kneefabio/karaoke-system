@echo off
chcp 65001 >nul
SETLOCAL EnableDelayedExpansion

title Setup Sistema Karaoke - Fix Python

echo ========================================
echo   SETUP CON FIX PYTHON 3.11
echo ========================================
echo.
echo Questo script forza l'uso di Python 3.11
echo.
pause

REM Trova Python 3.11
set PYTHON_PATH=
for %%p in (
    "C:\Program Files\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Python311\python.exe"
) do (
    if exist %%p (
        set PYTHON_PATH=%%~p
        goto :found_python
    )
)

echo [ERRORE] Non trovo Python 3.11!
echo.
echo Ho cercato in:
echo - C:\Program Files\Python311\
echo - C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\
echo - C:\Python311\
echo.
echo Installa Python 3.11 da:
echo https://www.python.org/downloads/release/python-3119/
echo.
pause
exit /b 1

:found_python
echo [OK] Python 3.11 trovato: %PYTHON_PATH%
echo.

REM Verifica versione
"%PYTHON_PATH%" --version
echo.

REM Verifica Node
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Node.js non trovato!
    pause
    exit /b 1
)
echo [OK] Node.js trovato
echo.

REM Setup Backend
echo [1/3] Configurazione Backend...
echo.

cd backend

if exist "venv" (
    echo Rimozione ambiente virtuale vecchio...
    rmdir /s /q venv
)

echo Creazione ambiente virtuale con Python 3.11...
"%PYTHON_PATH%" -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Impossibile creare ambiente virtuale
    cd ..
    pause
    exit /b 1
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo.
echo Installazione dipendenze Python...
echo (questo puo richiedere 2-3 minuti)
echo.
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Installazione fallita
    echo.
    cd ..
    pause
    exit /b 1
)

echo.
echo [OK] Backend configurato

(
    echo MONGO_URL=mongodb://localhost:27017
    echo DB_NAME=karaoke_db
    echo CORS_ORIGINS=http://localhost:3000
    echo JWT_SECRET=karaoke_secret_key_change_in_production
) > .env

cd ..
echo.

REM Setup Frontend
echo [2/3] Configurazione Frontend...
echo.

cd frontend

echo Installazione dipendenze Node.js...
echo (questo puo richiedere 3-5 minuti)
echo.
call yarn install
if %ERRORLEVEL% NEQ 0 (
    echo [ERRORE] Installazione fallita
    cd ..
    pause
    exit /b 1
)

echo.
echo [OK] Frontend configurato

(
    echo REACT_APP_BACKEND_URL=http://localhost:8001
) > .env

cd ..
echo.

REM Crea script di avvio
echo [3/3] Creazione script di avvio...
echo.

(
    echo @echo off
    echo title Karaoke Backend
    echo cd backend
    echo call venv\Scripts\activate.bat
    echo echo Backend in esecuzione su http://localhost:8001
    echo echo Premi Ctrl+C per fermare
    echo echo.
    echo uvicorn server:app --reload --host 0.0.0.0 --port 8001
    echo pause
) > start-backend.bat

(
    echo @echo off
    echo title Karaoke Frontend
    echo cd frontend
    echo echo Frontend in esecuzione su http://localhost:3000
    echo echo Premi Ctrl+C per fermare
    echo echo.
    echo yarn start
    echo pause
) > start-frontend.bat

(
    echo @echo off
    echo chcp 65001 ^>nul
    echo title Sistema Karaoke
    echo cls
    echo echo ========================================
    echo echo   SISTEMA PRENOTAZIONI KARAOKE
    echo echo ========================================
    echo echo.
    echo echo Pagina Pubblica:  http://localhost:3000
    echo echo Dashboard Admin:  http://localhost:3000/admin/login
    echo echo API Docs:         http://localhost:8001/docs
    echo echo.
    echo echo Admin: username=admin, password=admin123
    echo echo.
    echo echo ========================================
    echo echo.
    echo pause
    echo.
    echo start "Karaoke Backend" cmd /k "cd backend ^&^& venv\Scripts\activate.bat ^&^& uvicorn server:app --reload --host 0.0.0.0 --port 8001"
    echo timeout /t 5 /nobreak ^>nul
    echo cd frontend
    echo yarn start
) > start-all.bat

echo [OK] Script creati
echo.

if not exist "%USERPROFILE%\data\db" mkdir "%USERPROFILE%\data\db"

echo.
echo ========================================
echo    SETUP COMPLETATO!
echo ========================================
echo.
echo Per avviare: doppio click su start-all.bat
echo.
pause
