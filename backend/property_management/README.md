# Property Management System - Django Backend

This is the Django backend for the Property Management System.

## Environment Configuration

The application uses environment variables for configuration to separate development and production settings.

### Development Environment

For local development, use the `.env.development` file as a template. Copy it to `.env`:

```bash
cp .env.development .env
```

### Production Environment

For production deployment, use the `.env.production.example` file as a template. Copy it to `.env.production` and fill in your actual values:

```bash
cp .env.production.example .env.production
```

### Environment Variables

Key environment variables include:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL (for production)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database connection details (for development)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: Email configuration
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Project Structure

```
property_management/
├── config/                 # Django project settings
├── apps/                   # Django apps
│   ├── users/              # User management
│   ├── properties/         # Property management
│   ├── units/              # Unit/Room management
│   ├── tenants/            # Tenant management
│   ├── maintenance/        # Maintenance request management
│   └── payments/           # Payment tracking
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies

## Setup Instructions

1. **Navigate to the backend directory:**
   ```bash
   cd backend/property_management
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   For development, copy `.env.development` to `.env`:
   ```bash
   cp .env.development .env
   ```
   
   For production, copy `.env.production.example` to `.env.production` and fill in your actual values:
   ```bash
   cp .env.production.example .env.production
   ```
   
   Then configure your database settings and other environment variables as needed.

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
   Or use the default admin user:
   - Username: admin
   - Email: admin@example.com
   - Password: admin

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   
   For production, use the production settings:
   ```bash
   python manage.py runserver --settings=config.production_settings
   ```

## API Endpoints

### Authentication
- `POST /api/users/login/` - User login
  - Request Body: `{ "username": "string", "password": "string" }`
  - Response: `{ "token": "string", "user": { ... } }`
  - Permissions: Public

- `POST /api/users/logout/` - User logout
  - Response: `{ "message": "Logged out successfully" }`
  - Permissions: Authenticated users

### Users
- `GET /api/users/` - List all users
  - Response: Array of user objects
  - Permissions: Admin only

- `POST /api/users/` - Create a new user
  - Request Body: `{ "username": "string", "email": "string", "password": "string" }`
  - Response: User object
  - Permissions: Public

- `GET /api/users/{id}/` - Retrieve a user
  - Response: User object
  - Permissions: Authenticated users

- `PUT /api/users/{id}/` - Update a user
  - Request Body: `{ "username": "string", "email": "string", "role": "string", "is_approved": boolean }`
  - Response: Updated user object
  - Permissions: Admin only for role/is_approved changes

- `DELETE /api/users/{id}/` - Delete a user
  - Response: `{ "message": "User deleted successfully" }`
  - Permissions: Admin only

### Properties
- `GET /api/properties/` - List properties
  - Response: Array of property objects
  - Permissions: Authenticated users (Admin sees all, Property Owners see only their own)

- `POST /api/properties/` - Create a new property
  - Request Body: `{ "name": "string", "type": "string", "address": "string", "owner": integer }`
  - Response: Property object
  - Permissions: Admin only

- `GET /api/properties/{id}/` - Retrieve a property
  - Response: Property object
  - Permissions: Authenticated users (Admin sees all, Property Owners see only their own)

- `PUT /api/properties/{id}/` - Update a property
  - Request Body: `{ "name": "string", "type": "string", "address": "string" }`
  - Response: Updated property object
  - Permissions: Admin only

- `DELETE /api/properties/{id}/` - Delete a property
  - Response: `{ "message": "Property deleted successfully" }`
  - Permissions: Admin only

### Units
- `GET /api/units/` - List units
  - Response: Array of unit objects
  - Permissions: Property Owners (own properties only) and Admin

- `POST /api/units/` - Create a new unit
  - Request Body: `{ "unit_number": "string", "type": "string", "capacity": integer, "price": number, "status": "string", "property": integer }`
  - Response: Unit object
  - Permissions: Property Owners (own properties only)

- `GET /api/units/{id}/` - Retrieve a unit
  - Response: Unit object
  - Permissions: Property Owners (own properties only) and Admin

- `PUT /api/units/{id}/` - Update a unit
  - Request Body: `{ "unit_number": "string", "type": "string", "capacity": integer, "price": number, "status": "string" }`
  - Response: Updated unit object
  - Permissions: Property Owners (own properties only)

- `DELETE /api/units/{id}/` - Delete a unit
  - Response: `{ "message": "Unit deleted successfully" }`
  - Permissions: Property Owners (own properties only)

### Tenants
- `GET /api/tenants/` - List tenants
  - Response: Array of tenant objects
  - Permissions: Property Owners (own properties only) and Admin

- `POST /api/tenants/` - Create a new tenant
  - Request Body: `{ "first_name": "string", "last_name": "string", "email": "string", "phone": "string", "lease_start": "date", "lease_end": "date", "rent_amount": number, "deposit_amount": number, "unit": integer }`
  - Response: Tenant object
  - Permissions: Property Owners (own properties only)

- `GET /api/tenants/{id}/` - Retrieve a tenant
  - Response: Tenant object
  - Permissions: Property Owners (own properties only) and Admin

- `PUT /api/tenants/{id}/` - Update a tenant
  - Request Body: `{ "first_name": "string", "last_name": "string", "email": "string", "phone": "string", "lease_start": "date", "lease_end": "date", "rent_amount": number, "deposit_amount": number }`
  - Response: Updated tenant object
  - Permissions: Property Owners (own properties only)

- `DELETE /api/tenants/{id}/` - Delete a tenant
  - Response: `{ "message": "Tenant deleted successfully" }`
  - Permissions: Property Owners (own properties only)

### Maintenance Requests
- `GET /api/maintenance/` - List maintenance requests
  - Response: Array of maintenance request objects
  - Permissions: Property Owners (own properties only) and Admin

- `POST /api/maintenance/` - Create a new maintenance request
  - Request Body: `{ "title": "string", "description": "string", "priority": "string", "status": "string", "unit": integer, "submitted_by": integer }`
  - Response: Maintenance request object
  - Permissions: Property Owners (own properties only)

- `GET /api/maintenance/{id}/` - Retrieve a maintenance request
  - Response: Maintenance request object
  - Permissions: Property Owners (own properties only) and Admin

- `PUT /api/maintenance/{id}/` - Update a maintenance request
  - Request Body: `{ "title": "string", "description": "string", "priority": "string", "status": "string" }`
  - Response: Updated maintenance request object
  - Permissions: Property Owners (own properties only) and Admin

- `DELETE /api/maintenance/{id}/` - Delete a maintenance request
  - Response: `{ "message": "Maintenance request deleted successfully" }`
  - Permissions: Property Owners (own properties only)

### Payments
- `GET /api/payments/` - List payments
  - Response: Array of payment objects
  - Permissions: Property Owners (own properties only) and Admin

- `POST /api/payments/` - Create a new payment
  - Request Body: `{ "amount": number, "payment_date": "date", "payment_method": "string", "description": "string", "tenant": integer }`
  - Response: Payment object
  - Permissions: Property Owners (own properties only)

- `GET /api/payments/{id}/` - Retrieve a payment
  - Response: Payment object
  - Permissions: Property Owners (own properties only) and Admin

- `PUT /api/payments/{id}/` - Update a payment
  - Request Body: `{ "amount": number, "payment_date": "date", "payment_method": "string", "description": "string" }`
  - Response: Updated payment object
  - Permissions: Property Owners (own properties only)

- `DELETE /api/payments/{id}/` - Delete a payment
  - Response: `{ "message": "Payment deleted successfully" }`
  - Permissions: Property Owners (own properties only)

## Admin Module API Endpoints

### Dashboard
- `GET /api/admin-module/dashboard-stats/` - Get admin dashboard statistics
  - Response: `{ "totalOwners": integer, "totalProperties": integer, "pendingApprovals": integer, "activeTenants": integer }`
  - Permissions: Admin only

### Reports
- `GET /api/admin-module/reports/` - Get admin reports
  - Query Parameters:
    - `type`: "summary", "revenue", "occupancy", "maintenance", "tenants"
    - `start_date`: YYYY-MM-DD (optional)
    - `end_date`: YYYY-MM-DD (optional)
    - `property_id`: integer (optional)
  - Response: Report data based on type
  - Permissions: Admin only

### Settings
- `GET /api/admin-module/settings/` - Get admin settings
  - Response: Settings object with company info, currency, notifications, etc.
  - Permissions: Admin only

- `PATCH /api/admin-module/settings/` - Update admin settings
  - Request Body: Partial settings object
  - Response: Updated settings object
  - Permissions: Admin only

## Property Owner Module API Endpoints

### Dashboard
- `GET /api/property-owner-module/dashboard-stats/` - Get property owner dashboard statistics
  - Response: `{ "myProperties": integer, "totalUnits": integer, "occupiedUnits": integer, "pendingRequests": integer }`
  - Permissions: Property Owner only

### Reports
- `GET /api/property-owner-module/reports/` - Get property owner reports
  - Query Parameters:
    - `type`: "summary", "income", "occupancy", "maintenance", "tenants"
    - `start_date`: YYYY-MM-DD (optional)
    - `end_date`: YYYY-MM-DD (optional)
    - `property_id`: integer (optional)
  - Response: Report data based on type
  - Permissions: Property Owner only

## Database Schema

The database schema includes tables for:
- Users (admins and property owners)
- Properties
- Units/Rooms
- Tenants
- Maintenance Requests
- Payments

## Roles

1. **Admin**: Can see all activities and approve property owner account requests
2. **Property Owner**: Can manage their own properties after approval

## Testing the API

To test the API endpoints, you can use tools like curl, Postman, or write simple scripts:

```python
import requests

# Test the users API endpoint
response = requests.get('http://127.0.0.1:8000/api/users/')
print(response.json())
```

## Admin Interface

Django provides a built-in admin interface that can be accessed at:
- URL: http://127.0.0.1:8000/admin/
- Username: admin
- Password: admin