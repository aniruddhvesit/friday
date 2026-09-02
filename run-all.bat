@echo off
echo Starting Tyler Backend and Frontend...
start "Tyler Backend (FastAPI)" cmd /c "%~dp0run-backend.bat"
start "Tyler Frontend (Vite)" cmd /c "%~dp0run-frontend.bat"
echo Both servers launched in separate windows.
