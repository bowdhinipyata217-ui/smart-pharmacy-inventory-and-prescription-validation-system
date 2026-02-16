@echo off
echo ========================================
echo Pharmacy AI - Quick Start Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed!
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file with your configuration!
    echo Press any key to continue after editing .env...
    pause >nul
    echo.
)

REM Run migrations
echo Running database migrations...
python manage.py migrate
echo.

REM Check if superuser exists (optional check)
echo Starting Django development server...
echo.
echo Server will be available at: http://localhost:8000
echo Press CTRL+C to stop the server
echo.

REM Start Django server
python manage.py runserver

pause
