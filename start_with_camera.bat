@echo off
REM Quick start script for local development with camera support

echo ========================================
echo   Object Detection - Local Setup
echo   (With Camera Support)
echo ========================================
echo.

echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.11
    pause
    exit /b 1
)

echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found! Please install Node.js
    pause
    exit /b 1
)

echo.
echo [1/4] Installing backend dependencies...
cd backend
if not exist "yolov8m.pt" (
    echo NOTE: YOLO model will be downloaded on first run
)
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo [2/4] Installing frontend dependencies...
cd ..\frontend
if not exist "node_modules" (
    echo Installing npm packages (this may take a few minutes)...
    npm install
) else (
    echo npm packages already installed
)

echo [3/4] Configuring frontend for local backend...
echo REACT_APP_API_URL=http://localhost:5000 > .env.local
echo Created .env.local with local backend URL

echo.
echo [4/4] Starting services...
echo.
echo ========================================
echo   Starting Backend (localhost:5000)
echo ========================================
cd ..\backend
start "Object Detection Backend" cmd /k "python app.py"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   Starting Frontend (localhost:3000)
echo ========================================
cd ..\frontend
start "Object Detection Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Two terminal windows will open:
echo   1. Backend server (Flask + YOLO)
echo   2. Frontend server (React)
echo.
echo Your browser will open automatically to:
echo   http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop servers
echo.
echo ========================================
pause
