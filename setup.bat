@echo off
echo ========================================
echo   AI Object Detection - Setup Script
echo   Full Stack Edition
echo ========================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)
echo [OK] Python found
python --version
echo.

REM Check Node.js
echo [2/4] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 16+ first.
    pause
    exit /b 1
)
echo [OK] Node.js found
node --version
echo.

REM Setup Backend
echo [3/4] Setting up Backend...
cd backend

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

cd ..
echo [OK] Backend setup complete
echo.

REM Setup Frontend
echo [4/4] Setting up Frontend...
cd frontend

echo Installing Node dependencies (this may take a few minutes)...
call npm install

cd ..
echo [OK] Frontend setup complete
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   1. Double-click: start.bat
echo   OR
echo   2. Manual start:
echo      - Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python app.py
echo      - Frontend: cd frontend ^&^& npm start
echo.
echo Standalone mode (no frontend):
echo   python detection2.py
echo.
echo Press any key to exit...
pause >nul
