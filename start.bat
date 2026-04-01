@echo off
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo --------------------------------------
echo Starting TicketFlow NLP Routing System
echo --------------------------------------
echo.

:: Setup Virtual Environment if it doesn't exist or dependencies aren't installed
IF EXIST "venv\.installed" GOTO start_server

echo First-time setup: Checking virtual environment...
IF EXIST "venv\Scripts\activate.bat" GOTO install_deps
echo Creating virtual environment...
python -m venv venv
:install_deps
echo Installing or verifying required dependencies...
:: Use explicit path to the venv python to bypass Windows Store aliases
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
IF ERRORLEVEL 1 (
    echo.
    echo =======================================================
    echo ERROR: Python packages failed to install!
    echo Please scroll up and read the red errors above.
    echo Take a screenshot of the RED TEXT and show your team.
    echo =======================================================
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo done > venv\.installed
echo.

:start_server

:: Step 1. Start the Flask Backend Server in a separate window
echo Starting the Python Backend Server...
cd backend
start "TicketFlow Backend" cmd /k "..\venv\Scripts\python.exe app.py"
cd /d "%SCRIPT_DIR%"

:: Step 2. Wait 3 seconds to let the server boot up
ping 127.0.0.1 -n 4 > nul

:: Step 3. Open the Frontend naturally in your default browser
echo Opening Frontend UI...
start "" "%SCRIPT_DIR%frontend\signup.html"

echo.
echo Setup Complete! The backend is running securely in the new black window.
echo You can minimize that window, but DO NOT close it while using the app.