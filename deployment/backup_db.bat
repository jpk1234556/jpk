@echo off
:: Database Backup Script for Property Management System (Windows)
:: This script creates backups of the PostgreSQL database

echo === Property Management System Database Backup Script ===

:: Configuration
set DB_NAME=property_management
set DB_USER=pm_user
set DB_HOST=localhost
set DB_PORT=5432
set BACKUP_DIR=C:\backups\property-management\db

:: Get timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set TIMESTAMP=%dt:~0,8%_%dt:~8,6%

set BACKUP_FILE=%BACKUP_DIR%\pm_backup_%TIMESTAMP%.sql

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

:: Create backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Create database backup
call :print_status "Creating database backup..."
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% > "%BACKUP_FILE%"

if %errorlevel% equ 0 (
    call :print_status "Database backup created successfully: %BACKUP_FILE%"
) else (
    call :print_error "Failed to create database backup"
    exit /b 1
)

:: Compress the backup
call :print_status "Compressing backup file..."
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.GZipStream]::CreateFromDirectory('%BACKUP_FILE%', '%BACKUP_FILE%.gz') }"

if %errorlevel% equ 0 (
    call :print_status "Backup compressed successfully: %BACKUP_FILE%.gz"
    del "%BACKUP_FILE%"
) else (
    call :print_warning "Failed to compress backup file"
)

call :print_status "Database backup process completed!"