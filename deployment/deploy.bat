@echo off
:: Production Deployment Script for Property Management System (Windows)
:: This script automates the deployment process for the Django backend on Windows

echo === Property Management System Deployment Script ===
echo Starting deployment process...

:: Configuration
set PROJECT_DIR=C:\inetpub\wwwroot\property-management
set VENV_DIR=%PROJECT_DIR%\venv
set BACKEND_DIR=%PROJECT_DIR%\backend\property_management

:: Function to print status
:print_status
echo [INFO] %~1
goto :eof

:: Function to print warning
:print_warning
echo [WARNING] %~1
goto :eof

:: Function to print error
:print_error
echo [ERROR] %~1
goto :eof

:: 1. Backup current deployment
call :print_status "Creating backup of current deployment..."
set TIMESTAMP=%DATE:~-4%%DATE:~4,2%%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set BACKUP_DIR=C:\backups\property-management\%TIMESTAMP%
mkdir "%BACKUP_DIR%" 2>nul
xcopy "%PROJECT_DIR%" "%BACKUP_DIR%\" /E /I /H /Y >nul 2>&1
if errorlevel 1 (
    call :print_warning "Could not create backup"
)

:: 2. Update code from repository
call :print_status "Updating code from repository..."
cd /d "%PROJECT_DIR%"
git pull origin main
if errorlevel 1 (
    call :print_error "Failed to pull from repository"
    exit /b 1
)

:: 3. Activate virtual environment
call :print_status "Activating virtual environment..."
if not exist "%VENV_DIR%" (
    call :print_status "Creating virtual environment..."
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    call :print_error "Failed to activate virtual environment"
    exit /b 1
)

:: 4. Install/update dependencies
call :print_status "Installing/updating dependencies..."
pip install -r "%BACKEND_DIR%\requirements.txt"
if errorlevel 1 (
    call :print_error "Failed to install dependencies"
    exit /b 1
)

:: 5. Run database migrations
call :print_status "Running database migrations..."
cd /d "%BACKEND_DIR%"
python manage.py makemigrations
if errorlevel 1 (
    call :print_error "Failed to create migrations"
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    call :print_error "Failed to apply migrations"
    exit /b 1
)

:: 6. Collect static files
call :print_status "Collecting static files..."
python manage.py collectstatic --noinput
if errorlevel 1 (
    call :print_error "Failed to collect static files"
    exit /b 1
)

:: 7. Run tests
call :print_status "Running tests..."
python manage.py test
if errorlevel 1 (
    call :print_error "Tests failed"
    exit /b 1
)

:: 8. Restart services
call :print_status "Restarting services..."
:: Assuming you're using IIS or similar
:: iisreset
:: Uncomment the above line if using IIS

call :print_status "Deployment completed successfully!"
echo Backup stored at: %BACKUP_DIR%