@echo off
echo --------------------------------------
echo Starting TicketFlow NLP Routing System
echo --------------------------------------
echo.

:: Setup Virtual Environment if it doesn't exist or dependencies aren't installed
IF NOT EXIST "venv\.installed" (
    echo First-time setup: Checking virtual environment...
    IF NOT EXIST "venv\Scripts\activate.bat" (
        echo Creating virtual environment...
        python -m venv venv
    )
    
    echo Installing or verifying required dependencies...
    call venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    
    IF %ERRORLEVEL% EQU 0 (
        echo Dependencies installed successfully!
        echo done > venv\.installed
    ) ELSE (
        echo Error installing dependencies. Please check the terminal for details.
        pause
    )
    echo.
)

:: Step 1. Start the Flask Backend Server in a separate window
echo Starting the Python Backend Server...
cd backend
start "TicketFlow Backend" cmd /k "..\venv\Scripts\activate && python app.py"
cd ..

:: Step 2. Wait 3 seconds to let the server boot up
ping 127.0.0.1 -n 4 > nul

:: Step 3. Open the Frontend naturally in your default browser
echo Opening Frontend UI...
cd frontend
start signup.html

echo.
echo Setup Complete! The backend is running securely in the new black window.
echo You can minimize that window, but DO NOT close it while using the app.