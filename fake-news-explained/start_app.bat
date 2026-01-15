@echo off
TITLE Fake News Detector - Launcher
echo ==========================================
echo    STARTING FAKE NEWS DETECTOR
echo ==========================================

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Start Backend in a new minimized window
echo [1/2] Starting Backend Server (Python)...
start "Backend - Fake News Detector" /min cmd /c "cd backend && python app.py"

:: Wait a few seconds for backend to initialize
timeout /t 3 /nobreak > nul

:: Open the website in the default browser
echo [2/2] Opening Website...
echo Note: The small backend window must stay open while using the app.
start "" "index.html"

echo.
echo ==========================================
echo    APP IS RUNNING!
echo ==========================================
echo If the website didn't open, double-click 'index.html' manually.
echo Do not close the minimized 'Backend' window.
echo.
pause

