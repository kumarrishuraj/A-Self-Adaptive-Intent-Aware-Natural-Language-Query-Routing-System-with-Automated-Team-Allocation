@echo off
echo --------------------------------------
echo Starting TicketFlow NLP Routing System
echo --------------------------------------
echo.

:: Step 1. Start the Flask Backend Server in a separate window
echo Starting the Python Backend Server...
cd backend
start "TicketFlow Backend" cmd /k "..\venv\Scripts\activate && python app.py"
cd ..

:: Step 2. Wait 3 seconds to let the server boot up
timeout /t 3 /nobreak >nul

:: Step 3. Open the Frontend naturally in your default browser
echo Opening Frontend UI...
cd frontend
start signup.html

echo.
echo Setup Complete! The backend is running securely in the new black window.
echo You can minimize that window, but DO NOT close it while using the app.
