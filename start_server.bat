@echo off
TITLE FeWo Verwaltung Server

REM --- CONFIGURATION ---
REM We force the script to use the Anaconda Python found in your logs
SET "PYTHON_EXEC=c:\users\rkre7\anaconda3\python.exe"
REM ---------------------

echo Starting FeWo Verwaltung...
echo Using Python at: "%PYTHON_EXEC%"
echo.

REM Ensure we are in the script's directory
cd /d "%~dp0"

echo Checking dependencies...
REM We use the specific python executable to run pip
"%PYTHON_EXEC%" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Could not install dependencies.
    echo Please check if the path in 'PYTHON_EXEC' matches your Anaconda installation.
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
"%PYTHON_EXEC%" manage.py runserver

pause