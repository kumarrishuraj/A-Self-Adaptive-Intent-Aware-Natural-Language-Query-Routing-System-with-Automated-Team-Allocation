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
:: Step 1. Open the Frontend UI using Python (100% reliable across environments)
echo Opening Frontend UI...
venv\Scripts\python.exe -c "import webbrowser, os; webbrowser.open('file:///' + os.path.abspath('frontend/signup.html').replace('\\', '/'))"

:: Step 2. Start the Flask Backend Server in the CURRENT terminal window
echo.
echo Starting the Python Backend Server...
echo The server logs will appear below. Keep this window open!
echo -------------------------------------------------------------
cd backend
..\venv\Scripts\python.exe app.py