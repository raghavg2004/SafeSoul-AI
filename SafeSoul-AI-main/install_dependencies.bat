@echo off
REM ============================================================
REM SafeSoul AI Mental Health Chatbot - Dependency Installer
REM ============================================================
REM This batch file sets up the project environment and installs
REM all required Python dependencies for Windows systems.
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  SafeSoul AI - Mental Health Chatbot
echo  Dependency Installation Script
echo ============================================================
echo.

REM Color codes
set COLOR_GREEN=92
set COLOR_YELLOW=93
set COLOR_RED=91

REM Check if Python is installed
echo [1/5] Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo Please download Python 3.11+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [✓] %PYTHON_VERSION% found
echo.

REM Check if requirements.txt exists
echo [2/5] Checking requirements.txt...
if not exist "requirements.txt" (
    echo.
    echo ERROR: requirements.txt not found in current directory!
    echo Make sure you run this script from the project root folder.
    echo.
    pause
    exit /b 1
)
echo [✓] requirements.txt found
echo.

REM Create virtual environment if it doesn't exist
echo [3/5] Setting up Virtual Environment...
if not exist "venv" (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [4/5] Activating Virtual Environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)
echo [✓] Virtual environment activated
echo.

REM Upgrade pip
echo [5/5] Installing Dependencies...
echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.

REM Install requirements
echo Installing packages from requirements.txt...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  ✓ Installation Completed Successfully!
echo ============================================================
echo.
echo Next Steps:
echo -----------
echo 1. Create a .env file in the project root:
echo    - Add: GEMINI_API_KEY=your_api_key_here
echo    - Get your key from https://ai.google.dev/
echo.
echo 2. Run the application:
echo    streamlit run main.py
echo.
echo 3. The app will open at:
echo    http://localhost:8501
echo.
echo ============================================================
echo.

REM Verify installation
echo Verifying Installation...
pip list | findstr "streamlit google-generativeai pandas numpy"
if errorlevel 1 (
    echo WARNING: Some packages may not be installed correctly.
    echo Please check the output above for errors.
) else (
    echo [✓] Core packages verified
)

echo.
echo For more information, see README_SETUP.md
echo.
pause
