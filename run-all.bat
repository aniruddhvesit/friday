@echo off
title Tyler AI Assistant
echo ========================================================
echo               STARTING TYLER AI ASSISTANT               
echo ========================================================
echo.
echo [1/3] Starting Tyler FastAPI Backend...
start "Tyler Backend" /min cmd /c "%~dp0run-backend.bat"

echo [2/3] Starting Tyler Frontend Server...
start "Tyler Frontend" /min cmd /c "%~dp0run-frontend.bat"

echo [3/3] Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

echo Opening Tyler AI Assistant...

:: Open in standalone desktop app window mode if Edge or Chrome is available, else default browser
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:1420
) else if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://localhost:1420
) else (
    start http://localhost:1420
)

echo.
echo Tyler is now running at http://localhost:1420
exit
