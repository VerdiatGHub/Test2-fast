@echo off
title NeuralAgent Launcher

echo ==========================================
echo       NeuralAgent Startup Launcher
echo ==========================================
echo.

REM Check if backend .venv exists
if not exist "%~dp0backend\.venv" (
    echo [ERROR] Backend virtual environment not found!
    echo Please run setup_first_time.bat first.
    pause
    exit /b 1
)

REM Check if desktop venv exists
if not exist "%~dp0desktop\aiagent\venv" (
    echo [ERROR] Desktop agent virtual environment not found!
    echo Please run setup_first_time.bat first.
    pause
    exit /b 1
)

echo [1/2] Starting Backend FastAPI in a new window...
start "NeuralAgent Backend" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\activate.bat && python -m uvicorn main:app --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak
echo.

echo [2/2] Starting Electron Desktop App...
echo (The Python agent will start automatically when needed)
cd /d "%~dp0desktop"
call npm start

echo ==========================================
echo NeuralAgent has been closed.
echo ==========================================
pause
