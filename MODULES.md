# Property Management System - Module Structure

This document explains the two-module architecture of the Property Management System.

## Module Overview

The system is divided into two main modules:

1. **Admin Module** - For overall system administrators
2. **Property Owner Module** - For individual property owners

## Folder Structure

```
project/
├── backend/
│   ├── admin-module/
│   │   └── admin-api.js          # Admin API endpoints
│   ├── property-owner-module/
│   │   └── owner-api.js          # Property owner API endpoints
│   ├── server.js                 # Main server file
│   ├── package.json              # Backend dependencies
│   ├── database-schema.sql       # Database schema
│   └── .env                     # Environment variables
└── frontend/
    ├── admin-module/
    │   └── dashboard.html        # Admin dashboard UI
    ├── property-owner-module/
    │   └── dashboard.html        # Property owner dashboard UI
    └── public/                   # Shared frontend assets
        ├── index.html            # Main landing page
        ├── login.html            # Login page
        ├── landing.html          # Landing page
        ├── css/                  # Stylesheets
        └── js/                   # JavaScript files
```

## Admin Module

### Purpose
The Admin Module is designed for overall system administrators who need to:
- Monitor all activities across the system
- Approve new property owner account requests
- View all properties in the system
- Generate system-wide reports

### Key Features
- Dashboard with system-wide statistics
- Property owner approval system
- View all properties and their owners
- Recent activity tracking

### Access
- URL: `/frontend/admin-module/dashboard.html`
- API Endpoints: `/api/admin/*`

## Property Owner Module

### Purpose
The Property Owner Module is designed for individual property owners who need to:
- Manage their own properties
- View tenant information
- Handle maintenance requests
- Track payments and financials

### Key Features
- Dashboard with owner-specific statistics
- Property management for owned properties
- Tenant information and lease tracking
- Maintenance request handling
- Payment tracking

### Access
- URL: `/frontend/property-owner-module/dashboard.html`
- API Endpoints: `/api/owner/*`

## Authentication

The system uses role-based authentication:
- **Admin users** have access to the Admin Module
- **Property owners** have access to the Property Owner Module
- Users can only access the module corresponding to their role

## API Endpoints

### Admin Module Endpoints
- `GET /api/admin/dashboard-stats` - Get dashboard statistics
- `GET /api/admin/pending-owners` - Get pending property owners
- `POST /api/admin/approve-owner/:id` - Approve property owner
- `POST /api/admin/reject-owner/:id` - Reject property owner
- `GET /api/admin/properties` - Get all properties
- `GET /api/admin/recent-activity` - Get recent activity

### Property Owner Module Endpoints
- `GET /api/owner/dashboard-stats` - Get owner dashboard statistics
- `GET /api/owner/my-properties` - Get owner's properties
- `GET /api/owner/maintenance-requests` - Get maintenance requests
- `GET /api/owner/tenants` - Get tenants
- `GET /api/owner/payments` - Get payments

## Future Development

This modular structure allows for easy expansion:
- Additional modules can be added for other user roles
- Each module can be developed and deployed independently
- Shared components can be reused across modules