@echo off
REM Setup script for Property Management System Django Backend (Windows)

echo Setting up Property Management System Django Backend...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Instructions for creating superuser
echo.
echo Setup complete!
echo.
echo To create a superuser account, run:
echo   python manage.py createsuperuser
echo.
echo Follow the prompts to set your desired username, email, and password.
echo.
echo To start the server, run: python manage.py runserver
pause