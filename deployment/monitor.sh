#!/bin/bash

# Monitoring Script for Property Management System
# This script monitors the health and performance of the application

echo "=== Property Management System Monitoring Script ==="

# Configuration
APP_NAME="property-management"
LOG_DIR="/var/log/property-management"
MONITOR_LOG="$LOG_DIR/monitor.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log the monitoring execution
echo "[$TIMESTAMP] Starting monitoring checks..." >> "$MONITOR_LOG"

# 1. Check if the application is running
print_status "Checking application status..."
if pgrep -f "gunicorn" > /dev/null; then
    print_status "Application is running"
    echo "[$TIMESTAMP] Application is running" >> "$MONITOR_LOG"
else
    print_warning "Application is not running"
    echo "[$TIMESTAMP] Application is not running" >> "$MONITOR_LOG"
fi

# 2. Check disk space
print_status "Checking disk space..."
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    print_error "Disk usage is critical: ${DISK_USAGE}%"
    echo "[$TIMESTAMP] CRITICAL: Disk usage is ${DISK_USAGE}%" >> "$MONITOR_LOG"
elif [ "$DISK_USAGE" -gt 80 ]; then
    print_warning "Disk usage is high: ${DISK_USAGE}%"
    echo "[$TIMESTAMP] WARNING: Disk usage is ${DISK_USAGE}%" >> "$MONITOR_LOG"
else
    print_status "Disk usage is normal: ${DISK_USAGE}%"
    echo "[$TIMESTAMP] INFO: Disk usage is ${DISK_USAGE}%" >> "$MONITOR_LOG"
fi

# 3. Check memory usage
print_status "Checking memory usage..."
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
if [ "$MEMORY_USAGE" -gt 90 ]; then
    print_error "Memory usage is critical: ${MEMORY_USAGE}%"
    echo "[$TIMESTAMP] CRITICAL: Memory usage is ${MEMORY_USAGE}%" >> "$MONITOR_LOG"
elif [ "$MEMORY_USAGE" -gt 80 ]; then
    print_warning "Memory usage is high: ${MEMORY_USAGE}%"
    echo "[$TIMESTAMP] WARNING: Memory usage is ${MEMORY_USAGE}%" >> "$MONITOR_LOG"
else
    print_status "Memory usage is normal: ${MEMORY_USAGE}%"
    echo "[$TIMESTAMP] INFO: Memory usage is ${MEMORY_USAGE}%" >> "$MONITOR_LOG"
fi

# 4. Check CPU usage
print_status "Checking CPU usage..."
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')
if (( $(echo "$CPU_USAGE > 90" | bc -l) )); then
    print_error "CPU usage is critical: ${CPU_USAGE}%"
    echo "[$TIMESTAMP] CRITICAL: CPU usage is ${CPU_USAGE}%" >> "$MONITOR_LOG"
elif (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    print_warning "CPU usage is high: ${CPU_USAGE}%"
    echo "[$TIMESTAMP] WARNING: CPU usage is ${CPU_USAGE}%" >> "$MONITOR_LOG"
else
    print_status "CPU usage is normal: ${CPU_USAGE}%"
    echo "[$TIMESTAMP] INFO: CPU usage is ${CPU_USAGE}%" >> "$MONITOR_LOG"
fi

# 5. Check database connectivity
print_status "Checking database connectivity..."
# This is a simplified check - in practice, you'd want to test actual database queries
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    print_status "Database is accessible"
    echo "[$TIMESTAMP] INFO: Database is accessible" >> "$MONITOR_LOG"
else
    print_error "Database is not accessible"
    echo "[$TIMESTAMP] ERROR: Database is not accessible" >> "$MONITOR_LOG"
fi

# 6. Check recent error logs
print_status "Checking recent error logs..."
ERROR_COUNT=$(tail -100 "$LOG_DIR/django.log" | grep -c "ERROR")
if [ "$ERROR_COUNT" -gt 0 ]; then
    print_warning "Found $ERROR_COUNT recent errors in logs"
    echo "[$TIMESTAMP] WARNING: Found $ERROR_COUNT recent errors" >> "$MONITOR_LOG"
    # Show the last few errors
    tail -5 "$LOG_DIR/django.log" | grep "ERROR" >> "$MONITOR_LOG"
else
    print_status "No recent errors found"
    echo "[$TIMESTAMP] INFO: No recent errors found" >> "$MONITOR_LOG"
fi

print_status "Monitoring completed!"
echo "[$TIMESTAMP] Monitoring completed" >> "$MONITOR_LOG"