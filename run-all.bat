@echo off
if "%1"=="--debug" goto debug_mode
if "%1"=="-d" goto debug_mode

:: Default: Completely silent background launch with zero popups
wscript.exe "%~dp0launch-tyler.vbs"
exit /b

:debug_mode
title Tyler AI Assistant (Debug Console)
echo ========================================================
echo          STARTING TYLER AI ASSISTANT (DEBUG MODE)       
echo ========================================================
echo.
echo [1/3] Starting Tyler FastAPI Backend...
start "Tyler Backend" cmd /k "%~dp0run-backend.bat"

echo [2/3] Starting Tyler Frontend Server...
start "Tyler Frontend" cmd /k "%~dp0run-frontend.bat"

echo [3/3] Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:1420
) else if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://localhost:1420
) else (
    start http://localhost:1420
)
exit
