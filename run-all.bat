@echo off
echo Starting Friday Backend and Frontend...
start "Friday Backend (FastAPI)" cmd /c "%~dp0run-backend.bat"
start "Friday Frontend (Vite)" cmd /c "%~dp0run-frontend.bat"
echo Both servers launched in separate windows.
