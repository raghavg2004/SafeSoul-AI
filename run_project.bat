@echo off
setlocal
setlocal EnableDelayedExpansion

cd /d "%~dp0"

if not exist ".venv311\Scripts\python.exe" (
    echo Python virtual environment not found at .venv311.
    echo Create it first, then run this file again.
    pause
    exit /b 1
)

set "PORT=8501"

:find_port
netstat -ano | findstr /R /C:":!PORT! .*LISTENING" >nul
if errorlevel 1 goto launch

set /a PORT+=1
if !PORT! LEQ 8600 goto find_port

echo Could not find a free port between 8501 and 8600.
pause
exit /b 1

:launch

start "" "http://localhost:!PORT!"
".venv311\Scripts\python.exe" -m streamlit run "SafeSoul-AI-main\main.py" --server.port !PORT! --server.headless true

pause
