@echo off
title AI Fraud Detection System Startup
color 0A
echo.
echo ========================================
echo   AI Fraud Detection System Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated!
echo.

REM Install dependencies if needed
echo [2/4] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo [SUCCESS] Dependencies ready!
echo.

REM Start MLflow in new window
echo [3/4] Starting MLflow server...
start "MLflow Server" cmd /k "call venv\Scripts\activate.bat && mlflow server --host 127.0.0.1 --port 5001"
timeout /t 3 >nul
echo [SUCCESS] MLflow server started in new window!
echo.

REM Start Flask application
echo [4/4] Starting Flask application...
echo.
echo ========================================
echo   Starting AI Fraud Detection System
echo ========================================
echo.
echo MLflow Dashboard: http://127.0.0.1:5001
echo Main Application: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

python app.py

echo.
echo Application stopped. Press any key to exit...
pause >nul
