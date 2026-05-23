@echo off
setlocal

echo === SafeSoul-AI: setup installer ===

REM Change to the project folder containing requirements.txt
cd /d "%~dp0SafeSoul-AI-main" || (
  echo ERROR: Project folder not found: %~dp0SafeSoul-AI-main
  exit /b 1
)

REM Locate Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  where py >nul 2>&1
  if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found on PATH. Install Python 3.8+ and re-run this script.
    exit /b 1
  ) else (
    set "PYCMD=py -3"
  )
) else (
  set "PYCMD=python"
)

echo Using %PYCMD% to create virtual environment.
%PYCMD% --version

REM Create virtual environment if it doesn't exist
if not exist ".venv\Scripts\activate" (
  %PYCMD% -m venv .venv
)

REM Activate venv and install packages
call .venv\Scripts\activate

REM Ensure pip, wheel, setuptools and virtualenv are installed/upgraded
python -m pip install --upgrade pip setuptools wheel virtualenv

REM If virtualenv command exists, prefer creating venv with it (for reproducibility)
where virtualenv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  deactivate >nul 2>&1 || rem ignore if not active
  virtualenv .venv
  call .venv\Scripts\activate
)

REM Install exact versions from requirements.txt
if exist requirements.txt (
  pip install -r requirements.txt
) else (
  echo ERROR: requirements.txt not found in %CD%
  exit /b 1
)

echo.
echo Installation finished. To activate the venv:
echo    PowerShell:  .\.venv\Scripts\Activate.ps1
echo    CMD:         .\.venv\Scripts\activate.bat
echo.
endlocal
exit /b 0
