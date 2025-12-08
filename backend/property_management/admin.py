#!/usr/bin/env python
import os
import sys
import subprocess
import argparse

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def start_server():
    """Start the Django development server"""
    print("Starting Django development server...")
    os.system("python manage.py runserver")

def create_migration():
    """Create database migrations"""
    print("Creating database migrations...")
    code, stdout, stderr = run_command("python manage.py makemigrations")
    if code == 0:
        print("Migrations created successfully!")
        print(stdout)
    else:
        print("Error creating migrations:")
        print(stderr)

def apply_migrations():
    """Apply database migrations"""
    print("Applying database migrations...")
    code, stdout, stderr = run_command("python manage.py migrate")
    if code == 0:
        print("Migrations applied successfully!")
        print(stdout)
    else:
        print("Error applying migrations:")
        print(stderr)

def create_superuser():
    """Create a superuser"""
    print("Creating superuser...")
    os.system("python manage.py createsuperuser")

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    code, stdout, stderr = run_command("python manage.py collectstatic --noinput")
    if code == 0:
        print("Static files collected successfully!")
        print(stdout)
    else:
        print("Error collecting static files:")
        print(stderr)

def main():
    parser = argparse.ArgumentParser(description='Property Management System Admin Tool')
    parser.add_argument('command', choices=['start', 'migrate', 'makemigrations', 'createsuperuser', 'collectstatic'], 
                        help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        start_server()
    elif args.command == 'makemigrations':
        create_migration()
    elif args.command == 'migrate':
        apply_migrations()
    elif args.command == 'createsuperuser':
        create_superuser()
    elif args.command == 'collectstatic':
        collect_static()

if __name__ == '__main__':
    main()