@echo off
cd /d "C:\Users\hunte\OneDrive\Desktop\maya ui"
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else (
    echo [ERROR] .venv not found!
    echo Please ensure the virtual environment is set up.
    pause
)
exit
