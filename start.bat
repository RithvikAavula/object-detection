@echo off
echo ========================================
echo   AI Object Detection - Full Stack
echo   Starting Backend and Frontend
echo ========================================
echo.

REM Check if backend virtual environment exists
if not exist "backend\venv\" (
    echo [ERROR] Backend virtual environment not found!
    echo Please run setup first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules\" (
    echo [ERROR] Frontend dependencies not installed!
    echo Please run setup first:
    echo   cd frontend
    echo   npm install
    pause
    exit /b 1
)

echo [1/2] Starting Flask Backend...
echo.
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && python app.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo [2/2] Starting React Frontend...
echo.
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
echo (Servers will keep running in separate windows)
pause >nul
