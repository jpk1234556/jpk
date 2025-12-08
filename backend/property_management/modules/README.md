# Backend Modules Structure

This directory contains the organized backend modules that correspond to the frontend structure.

## Directory Structure

```
modules/
├── admin/                 # Admin module (corresponds to frontend/admin-module/)
│   ├── views/            # Admin-specific views
│   ├── serializers/      # Admin-specific serializers
│   └── urls.py           # Admin module URLs
└── property_owner/       # Property Owner module (corresponds to frontend/property-owner-module/)
    ├── views/            # Property Owner-specific views
    ├── serializers/      # Property Owner-specific serializers
    └── urls.py           # Property Owner module URLs
```

## Purpose

This structure mirrors the frontend organization to make it easier to:
1. Understand which backend code corresponds to which frontend pages
2. Maintain consistency between frontend and backend
3. Organize code by user role and functionality

## Module Responsibilities

### Admin Module
Handles all functionality for overall system administrators:
- Dashboard statistics
- Property owner approvals
- System-wide reports
- User management

### Property Owner Module
Handles all functionality for individual property owners:
- Property management
- Tenant information
- Maintenance requests
- Payment tracking

## API Endpoints

### Admin Module
- `/api/admin-module/dashboard-stats/` - Get admin dashboard statistics

### Property Owner Module
- `/api/property-owner-module/dashboard-stats/` - Get property owner dashboard statistics

## Future Development

Additional files will be added to each module as the corresponding frontend pages are implemented:
- Property owners management (admin)
- Properties management (both admin and property owner)
- Tenants management (property owner)
- Maintenance requests (property owner)
- Payments tracking (property owner)
- Reports (both)