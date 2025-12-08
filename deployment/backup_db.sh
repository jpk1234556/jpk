#!/bin/bash

# Database Backup Script for Property Management System
# This script creates backups of the PostgreSQL database

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Property Management System Database Backup Script ==="

# Configuration
DB_NAME="property_management"
DB_USER="pm_user"
DB_HOST="localhost"
DB_PORT="5432"
BACKUP_DIR="/var/backups/property-management/db"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/pm_backup_$TIMESTAMP.sql"

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

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create database backup
print_status "Creating database backup..."
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    print_status "Database backup created successfully: $BACKUP_FILE"
else
    print_error "Failed to create database backup"
    exit 1
fi

# Compress the backup
print_status "Compressing backup file..."
gzip "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    print_status "Backup compressed successfully: $BACKUP_FILE.gz"
else
    print_warning "Failed to compress backup file"
fi

# Remove backups older than 30 days
print_status "Removing old backups (older than 30 days)..."
find "$BACKUP_DIR" -name "pm_backup_*.sql*" -mtime +30 -delete

print_status "Database backup process completed!"