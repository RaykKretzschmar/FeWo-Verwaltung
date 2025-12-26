@echo off
TITLE FeWo Verwaltung Server

echo Starting FeWo Verwaltung...
echo.

REM Ensure we are in the script's directory
cd /d "%~dp0"

echo Checking/Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies. Please ensure Python is installed and added to PATH.
    pause
    exit /b
)

echo.
echo Navigating to project directory...
cd fewo_web\fewo

echo.
echo Opening browser...
start http://127.0.0.1:8000

echo.
echo Starting Django Server...
python manage.py runserver

pause
