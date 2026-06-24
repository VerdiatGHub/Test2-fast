@echo off
title NeuralAgent - First Time Setup

echo ==========================================
echo    NeuralAgent First Time Setup
echo ==========================================
echo.

echo [1/4] Setting up Backend virtual environment...
cd backend
if not exist .venv (
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
) else (
    echo Backend .venv already exists, skipping...
)
echo.

echo [2/4] Running database migrations...
.venv\Scripts\alembic upgrade head
echo.

echo [3/4] Setting up Desktop Agent virtual environment...
cd ..\desktop
if not exist aiagent\venv (
    python -m venv aiagent\venv
    aiagent\venv\Scripts\pip install -r aiagent\requirements.txt
) else (
    echo Desktop agent venv already exists, skipping...
)
echo.

echo [4/4] Installing Electron dependencies...
if not exist node_modules (
    call npm install
) else (
    echo Electron node_modules already exists, skipping...
)

cd neuralagent-app
if not exist node_modules (
    call npm install
) else (
    echo React app node_modules already exists, skipping...
)
cd ..

echo.
echo ==========================================
echo Setup complete!
echo.
echo Next steps:
echo 1. Make sure backend\.env is configured
echo 2. Create desktop\neuralagent-app\.env with backend URL
echo 3. Run run_neuralagent.bat to start the application
echo ==========================================
pause
