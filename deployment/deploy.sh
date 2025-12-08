#!/bin/bash

# Production Deployment Script for Property Management System
# This script automates the deployment process for the Django backend

set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Property Management System Deployment Script ==="
echo "Starting deployment process..."

# Configuration
PROJECT_DIR="/var/www/property-management"
VENV_DIR="$PROJECT_DIR/venv"
BACKEND_DIR="$PROJECT_DIR/backend/property_management"

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

# Check if running as root (recommended for production)
if [[ $EUID -eq 0 ]]; then
   print_warning "Running as root. This is not recommended for security reasons."
fi

# 1. Backup current deployment
print_status "Creating backup of current deployment..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/property-management/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"
cp -r "$PROJECT_DIR" "$BACKUP_DIR/" || print_warning "Could not create backup"

# 2. Update code from repository
print_status "Updating code from repository..."
cd "$PROJECT_DIR"
git pull origin main || { print_error "Failed to pull from repository"; exit 1; }

# 3. Activate virtual environment
print_status "Activating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate" || { print_error "Failed to activate virtual environment"; exit 1; }

# 4. Install/update dependencies
print_status "Installing/updating dependencies..."
pip install -r "$BACKEND_DIR/requirements.txt" || { print_error "Failed to install dependencies"; exit 1; }

# 5. Run database migrations
print_status "Running database migrations..."
cd "$BACKEND_DIR"
python manage.py makemigrations || { print_error "Failed to create migrations"; exit 1; }
python manage.py migrate || { print_error "Failed to apply migrations"; exit 1; }

# 6. Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput || { print_error "Failed to collect static files"; exit 1; }

# 7. Run tests
print_status "Running tests..."
python manage.py test || { print_error "Tests failed"; exit 1; }

# 8. Restart services
print_status "Restarting services..."
# Assuming you're using systemd or similar
sudo systemctl restart gunicorn || print_warning "Failed to restart gunicorn"
sudo systemctl restart nginx || print_warning "Failed to restart nginx"

# 9. Check service status
print_status "Checking service status..."
sudo systemctl status gunicorn || print_warning "Gunicorn status check failed"
sudo systemctl status nginx || print_warning "Nginx status check failed"

print_status "Deployment completed successfully!"
echo "Backup stored at: $BACKUP_DIR"