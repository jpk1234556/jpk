@echo off
:: Monitoring Script for Property Management System (Windows)
:: This script monitors the health and performance of the application

echo === Property Management System Monitoring Script ===

:: Configuration
set LOG_DIR=C:\logs\property-management
set TIMESTAMP=%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2% %TIME:~0,2%:%TIME:~3,2%:%TIME:~6,2%

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

:: Create log directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Log the monitoring execution
echo [%TIMESTAMP%] Starting monitoring checks... >> "%LOG_DIR%\monitor.log"

:: 1. Check if the application is running
call :print_status "Checking application status..."
tasklist | findstr python >nul
if %errorlevel% equ 0 (
    call :print_status "Application is running"
    echo [%TIMESTAMP%] Application is running >> "%LOG_DIR%\monitor.log"
) else (
    call :print_warning "Application is not running"
    echo [%TIMESTAMP%] Application is not running >> "%LOG_DIR%\monitor.log"
)

:: 2. Check disk space
call :print_status "Checking disk space..."
for /f "tokens=2 delims=:" %%a in ('fsutil volume diskfree C: ^| findstr "avail free"') do (
    set FREE_SPACE=%%a
)
:: Simplified check - in practice, you'd want a more precise calculation
call :print_status "Disk space check completed"
echo [%TIMESTAMP%] INFO: Disk space check completed >> "%LOG_DIR%\monitor.log"

:: 3. Check memory usage
call :print_status "Checking memory usage..."
wmic OS get FreePhysicalMemory /Value | findstr "=" >nul
if %errorlevel% equ 0 (
    call :print_status "Memory usage check completed"
    echo [%TIMESTAMP%] INFO: Memory usage check completed >> "%LOG_DIR%\monitor.log"
) else (
    call :print_warning "Unable to check memory usage"
    echo [%TIMESTAMP%] WARNING: Unable to check memory usage >> "%LOG_DIR%\monitor.log"
)

:: 4. Check database connectivity
call :print_status "Checking database connectivity..."
:: This is a simplified check - in practice, you'd want to test actual database queries
psql -h localhost -p 5432 -U postgres -c "SELECT 1;" >nul 2>&1
if %errorlevel% equ 0 (
    call :print_status "Database is accessible"
    echo [%TIMESTAMP%] INFO: Database is accessible >> "%LOG_DIR%\monitor.log"
) else (
    call :print_error "Database is not accessible"
    echo [%TIMESTAMP%] ERROR: Database is not accessible >> "%LOG_DIR%\monitor.log"
)

:: 5. Check recent error logs
call :print_status "Checking recent error logs..."
if exist "%LOG_DIR%\django.log" (
    findstr /C:"ERROR" "%LOG_DIR%\django.log" >nul
    if %errorlevel% equ 0 (
        call :print_warning "Recent errors found in logs"
        echo [%TIMESTAMP%] WARNING: Recent errors found >> "%LOG_DIR%\monitor.log"
    ) else (
        call :print_status "No recent errors found"
        echo [%TIMESTAMP%] INFO: No recent errors found >> "%LOG_DIR%\monitor.log"
    )
) else (
    call :print_warning "Log file not found"
    echo [%TIMESTAMP%] WARNING: Log file not found >> "%LOG_DIR%\monitor.log"
)

call :print_status "Monitoring completed!"
echo [%TIMESTAMP%] Monitoring completed >> "%LOG_DIR%\monitor.log"