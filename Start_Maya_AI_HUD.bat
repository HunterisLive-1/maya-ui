@echo off
cd /d "%~dp0"
echo Starting Maya AI HUD...
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if required packages are installed
python -c "import PySide6, psutil, GPUtil, pynvml" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install packages. Please check requirements.txt
        pause
        exit /b 1
    )
)

REM Start the application
echo Launching Maya AI HUD...
python main.py

if errorlevel 1 (
    echo.
    echo Application closed with error.
    pause
)
