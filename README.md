# Property Management System

A comprehensive property management system for property owners such as hostel, apartment, hotel, and rental owners.

## Project Structure

```
project/
├── backend/
│   ├── property_management/   # Django project directory
│   │   ├── manage.py          # Django management script
│   │   ├── requirements.txt   # Python dependencies
│   │   ├── config/            # Django settings
│   │   └── apps/              # Django apps (users, properties, etc.)
│   ├── database-schema.sql    # Database schema
│   └── .env                   # Environment variables
└── frontend/
    └── public/                # Frontend assets
        ├── index.html         # Main dashboard
        ├── properties.html    # Properties page
        ├── css/               # Stylesheets
        └── js/                # JavaScript files
```

## Features

- **Admin Dashboard**: Overall admin can see all activities and approve requests for property owner accounts
- **Property Owner Accounts**: Secondary admins for approved property owners
- **Property Management**: Manage multiple properties of different types
- **Unit Management**: Track rooms/units and their occupancy status
- **Tenant Management**: Maintain tenant information and lease details
- **Maintenance Requests**: Handle maintenance requests with priority levels
- **Payment Tracking**: Record and track tenant payments

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django (Python) with Django REST Framework
- **Database**: PostgreSQL (Supabase)

## Color Scheme

- Primary Colors: White and Orange

## Setup Instructions

1. Navigate to the backend directory:
   ```bash
   cd backend/property_management
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables in `backend/.env` file

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

9. Open your browser to `http://localhost:8000`

## Database Schema

The database schema is defined in `backend/database-schema.sql` and includes tables for:
- Users (admins and property owners)
- Properties
- Units/Rooms
- Tenants
- Maintenance Requests
- Payments

## Roles

1. **Overall Admin**: Can see all activities and approve property owner account requests
2. **Property Owners**: Secondary admins for their own properties after approval

## API Endpoints

- `/api/health` - Health check endpoint

*(More endpoints will be added as the system develops)*