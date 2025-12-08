#!/bin/bash

# Setup script for Property Management System Django Backend

echo "Setting up Property Management System Django Backend..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Setup complete!"
echo "To start the server, run: python manage.py runserver"