@echo off
:: Start the HUD UI automatically
start "" "C:\Users\hunte\OneDrive\Desktop\maya ui\ui.bat"

cd /d "c:\Users\hunte\OneDrive\Desktop\hunter ai maya v2"
call venv\Scripts\activate

:menu
cls
echo ==========================================
echo           Maya AI Launcher 🚀
echo ==========================================
echo.
echo [1] Console Mode (Normal Use)
echo [2] Dev Mode (LiveKit UI / Debugging)
echo [3] Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" goto console
if "%choice%"=="2" goto dev
if "%choice%"=="3" goto exit
echo Invalid choice!
pause
goto menu

:console
echo Starting Maya in Console Mode...
python main.py console
goto end

:dev
echo Starting Maya in Dev Mode...
python main.py dev
goto end

:end
echo.
echo Maya process finished.
pause
goto menu

:exit
exit
