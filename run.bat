@echo off
REM Creates a virtual environment, installs dependencies and starts the FastAPI server.
REM Usage:  run.bat
REM Options (set before running):  set PORT=9000   set HOST=0.0.0.0   set RELOAD=0

setlocal EnableExtensions

REM Always run from the folder this script lives in
cd /d "%~dp0"

set "VENV_DIR=venv"
if not defined HOST set "HOST=127.0.0.1"
if not defined PORT set "PORT=8002"
if not defined RELOAD set "RELOAD=1"

REM --- Checks ---------------------------------------------------------------
where python >nul 2>&1
if errorlevel 1 (
    echo Error: python is not installed or not on PATH.
    exit /b 1
)

if not exist requirements.txt (
    echo Error: requirements.txt not found in %CD%.
    exit /b 1
)

if not exist .env (
    echo Error: .env not found. Create it with at least:
    echo   GROQ_API_KEY=your_key_here
    exit /b 1
)

findstr /b /r /c:"GROQ_API_KEY=." .env >nul 2>&1
if errorlevel 1 (
    echo Error: GROQ_API_KEY is missing or empty in .env.
    exit /b 1
)

REM --- Virtual environment --------------------------------------------------
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment in .\%VENV_DIR% ...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Error: could not create the virtual environment.
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate.bat"

REM --- Dependencies (reinstall only when requirements.txt changed) ----------
set "STAMP=%VENV_DIR%\.requirements.hash"
set "CURRENT_HASH="
for /f "skip=1 tokens=* delims=" %%H in ('certutil -hashfile requirements.txt MD5 ^| findstr /v /c:"hash of" /c:"CertUtil"') do (
    if not defined CURRENT_HASH set "CURRENT_HASH=%%H"
)
set "CURRENT_HASH=%CURRENT_HASH: =%"

set "SAVED_HASH="
if exist "%STAMP%" set /p SAVED_HASH=<"%STAMP%"

if not "%CURRENT_HASH%"=="%SAVED_HASH%" (
    echo Installing dependencies ...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: dependency installation failed.
        exit /b 1
    )
    >"%STAMP%" echo %CURRENT_HASH%
) else (
    echo Dependencies are up to date.
)

REM --- Run the API ----------------------------------------------------------
echo Starting API at http://%HOST%:%PORT%  (docs: http://%HOST%:%PORT%/docs)

if "%RELOAD%"=="1" (
    uvicorn api:app --host %HOST% --port %PORT% --reload
) else (
    uvicorn api:app --host %HOST% --port %PORT%
)

endlocal