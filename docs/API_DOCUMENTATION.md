# Property Management System API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Users API](#users-api)
3. [Properties API](#properties-api)
4. [Units API](#units-api)
5. [Tenants API](#tenants-api)
6. [Maintenance Requests API](#maintenance-requests-api)
7. [Payments API](#payments-api)
8. [Admin Module API](#admin-module-api)
9. [Property Owner Module API](#property-owner-module-api)
10. [Health Check API](#health-check-api)

## Authentication

### Login
**Endpoint**: `POST /api/users/login/`
**Description**: Authenticate a user and receive an authentication token
**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
**Response**:
```json
{
  "token": "string",
  "user": {
    "id": 0,
    "username": "string",
    "email": "string",
    "role": "admin|property_owner",
    "is_approved": true,
    "date_joined": "datetime"
  }
}
```
**Status Codes**:
- 200: Successful login
- 400: Invalid credentials

### Logout
**Endpoint**: `POST /api/users/logout/`
**Description**: Invalidate the current user's authentication token
**Headers**: `Authorization: Token <token>`
**Response**:
```json
{
  "message": "Successfully logged out"
}
```
**Status Codes**:
- 200: Successful logout
- 401: Authentication required

## Users API

### List/Create Users
**Endpoint**: `GET/POST /api/users/`
**Description**: Get a list of all users (admin only) or create a new user
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "admin|property_owner",
  "is_approved": true
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "username": "string",
    "email": "string",
    "role": "admin|property_owner",
    "is_approved": true,
    "date_joined": "datetime"
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "role": "admin|property_owner",
  "is_approved": true,
  "date_joined": "datetime"
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required
- 403: Insufficient permissions

### Get/Update/Delete User
**Endpoint**: `GET/PUT/DELETE /api/users/{id}/`
**Description**: Get, update, or delete a specific user
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "username": "string",
  "email": "string",
  "role": "admin|property_owner",
  "is_approved": true
}
```
**Response**:
```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "role": "admin|property_owner",
  "is_approved": true,
  "date_joined": "datetime"
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 401: Authentication required
- 403: Insufficient permissions
- 404: User not found

## Properties API

### List/Create Properties
**Endpoint**: `GET/POST /api/properties/`
**Description**: Get a list of properties or create a new property (admin only)
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "name": "string",
  "type": "hostel|apartment|hotel|rental",
  "address": "string",
  "owner": 0
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "name": "string",
    "type": "hostel|apartment|hotel|rental",
    "address": "string",
    "owner": 0
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "name": "string",
  "type": "hostel|apartment|hotel|rental",
  "address": "string",
  "owner": 0
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required
- 403: Insufficient permissions

### Get/Update/Delete Property
**Endpoint**: `GET/PUT/DELETE /api/properties/{id}/`
**Description**: Get, update, or delete a specific property
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "name": "string",
  "type": "hostel|apartment|hotel|rental",
  "address": "string",
  "owner": 0
}
```
**Response**:
```json
{
  "id": 0,
  "name": "string",
  "type": "hostel|apartment|hotel|rental",
  "address": "string",
  "owner": 0
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 400: Validation error
- 401: Authentication required
- 403: Insufficient permissions
- 404: Property not found

## Units API

### List/Create Units
**Endpoint**: `GET/POST /api/units/`
**Description**: Get a list of units or create a new unit
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "unit_number": "string",
  "unit_type": "string",
  "capacity": 0,
  "price": 0,
  "status": "available|occupied|maintenance",
  "property": 0
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "unit_number": "string",
    "unit_type": "string",
    "capacity": 0,
    "price": 0,
    "status": "available|occupied|maintenance",
    "property": 0
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "unit_number": "string",
  "unit_type": "string",
  "capacity": 0,
  "price": 0,
  "status": "available|occupied|maintenance",
  "property": 0
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required

### Get/Update/Delete Unit
**Endpoint**: `GET/PUT/DELETE /api/units/{id}/`
**Description**: Get, update, or delete a specific unit
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "unit_number": "string",
  "unit_type": "string",
  "capacity": 0,
  "price": 0,
  "status": "available|occupied|maintenance",
  "property": 0
}
```
**Response**:
```json
{
  "id": 0,
  "unit_number": "string",
  "unit_type": "string",
  "capacity": 0,
  "price": 0,
  "status": "available|occupied|maintenance",
  "property": 0
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 400: Validation error
- 401: Authentication required
- 404: Unit not found

## Tenants API

### List/Create Tenants
**Endpoint**: `GET/POST /api/tenants/`
**Description**: Get a list of tenants or create a new tenant
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "lease_start": "date",
  "lease_end": "date",
  "rent_amount": 0,
  "deposit_amount": 0,
  "unit": 0
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "lease_start": "date",
    "lease_end": "date",
    "rent_amount": 0,
    "deposit_amount": 0,
    "unit": 0
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "lease_start": "date",
  "lease_end": "date",
  "rent_amount": 0,
  "deposit_amount": 0,
  "unit": 0
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required

### Get/Update/Delete Tenant
**Endpoint**: `GET/PUT/DELETE /api/tenants/{id}/`
**Description**: Get, update, or delete a specific tenant
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "lease_start": "date",
  "lease_end": "date",
  "rent_amount": 0,
  "deposit_amount": 0,
  "unit": 0
}
```
**Response**:
```json
{
  "id": 0,
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string",
  "lease_start": "date",
  "lease_end": "date",
  "rent_amount": 0,
  "deposit_amount": 0,
  "unit": 0
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 400: Validation error
- 401: Authentication required
- 404: Tenant not found

## Maintenance Requests API

### List/Create Maintenance Requests
**Endpoint**: `GET/POST /api/maintenance/`
**Description**: Get a list of maintenance requests or create a new request
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "status": "pending|in_progress|completed",
  "unit": 0
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "title": "string",
    "description": "string",
    "priority": "low|medium|high",
    "status": "pending|in_progress|completed",
    "unit": 0,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "status": "pending|in_progress|completed",
  "unit": 0,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required

### Get/Update/Delete Maintenance Request
**Endpoint**: `GET/PUT/DELETE /api/maintenance/{id}/`
**Description**: Get, update, or delete a specific maintenance request
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "status": "pending|in_progress|completed",
  "unit": 0
}
```
**Response**:
```json
{
  "id": 0,
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "status": "pending|in_progress|completed",
  "unit": 0,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 400: Validation error
- 401: Authentication required
- 404: Maintenance request not found

## Payments API

### List/Create Payments
**Endpoint**: `GET/POST /api/payments/`
**Description**: Get a list of payments or create a new payment
**Headers**: `Authorization: Token <token>`
**Request Body** (for POST):
```json
{
  "amount": 0,
  "payment_date": "date",
  "payment_method": "cash|check|bank_transfer|credit_card",
  "description": "string",
  "tenant": 0
}
```
**Response** (for GET):
```json
[
  {
    "id": 0,
    "amount": 0,
    "payment_date": "date",
    "payment_method": "cash|check|bank_transfer|credit_card",
    "description": "string",
    "tenant": 0,
    "created_at": "datetime"
  }
]
```
**Response** (for POST):
```json
{
  "id": 0,
  "amount": 0,
  "payment_date": "date",
  "payment_method": "cash|check|bank_transfer|credit_card",
  "description": "string",
  "tenant": 0,
    "created_at": "datetime"
}
```
**Status Codes**:
- 200: Successful GET request
- 201: Successful POST request
- 400: Validation error
- 401: Authentication required

### Get/Update/Delete Payment
**Endpoint**: `GET/PUT/DELETE /api/payments/{id}/`
**Description**: Get, update, or delete a specific payment
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "amount": 0,
  "payment_date": "date",
  "payment_method": "cash|check|bank_transfer|credit_card",
  "description": "string",
  "tenant": 0
}
```
**Response**:
```json
{
  "id": 0,
  "amount": 0,
  "payment_date": "date",
  "payment_method": "cash|check|bank_transfer|credit_card",
  "description": "string",
  "tenant": 0,
  "created_at": "datetime"
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 204: Successful DELETE request
- 400: Validation error
- 401: Authentication required
- 404: Payment not found

## Admin Module API

### Admin Dashboard Statistics
**Endpoint**: `GET /api/admin-module/dashboard-stats/`
**Description**: Get dashboard statistics for admin users
**Headers**: `Authorization: Token <token>`
**Response**:
```json
{
  "total_property_owners": 0,
  "total_properties": 0,
  "pending_approvals": 0,
  "active_tenants": 0
}
```
**Status Codes**:
- 200: Successful request
- 401: Authentication required
- 403: Insufficient permissions

### Admin Reports
**Endpoint**: `GET /api/admin-module/reports/`
**Description**: Get reports for admin users
**Headers**: `Authorization: Token <token>`
**Query Parameters**:
- `report_type`: String - Type of report (revenue, occupancy, maintenance, tenants)
- `start_date`: Date - Start date for the report
- `end_date`: Date - End date for the report
- `property_id`: Integer - Filter by specific property (optional)
**Response**:
```json
{
  "report_type": "string",
  "data": {}
}
```
**Status Codes**:
- 200: Successful request
- 400: Invalid parameters
- 401: Authentication required
- 403: Insufficient permissions

### Admin Settings
**Endpoint**: `GET/PUT /api/admin-module/settings/`
**Description**: Get or update admin settings
**Headers**: `Authorization: Token <token>`
**Request Body** (for PUT):
```json
{
  "company_name": "string",
  "address": "string",
  "phone": "string",
  "email": "string",
  "currency": "string",
  "timezone": "string"
}
```
**Response**:
```json
{
  "company_name": "string",
  "address": "string",
  "phone": "string",
  "email": "string",
  "currency": "string",
  "timezone": "string"
}
```
**Status Codes**:
- 200: Successful GET/PUT request
- 400: Validation error
- 401: Authentication required
- 403: Insufficient permissions

## Property Owner Module API

### Property Owner Dashboard Statistics
**Endpoint**: `GET /api/property-owner-module/dashboard-stats/`
**Description**: Get dashboard statistics for property owner users
**Headers**: `Authorization: Token <token>`
**Response**:
```json
{
  "my_properties": 0,
  "total_units": 0,
  "occupied_units": 0,
  "pending_requests": 0
}
```
**Status Codes**:
- 200: Successful request
- 401: Authentication required
- 403: Insufficient permissions

### Property Owner Reports
**Endpoint**: `GET /api/property-owner-module/reports/`
**Description**: Get reports for property owner users
**Headers**: `Authorization: Token <token>`
**Query Parameters**:
- `report_type`: String - Type of report (income, occupancy, maintenance, tenants)
- `start_date`: Date - Start date for the report
- `end_date`: Date - End date for the report
- `property_id`: Integer - Filter by specific property (optional)
**Response**:
```json
{
  "report_type": "string",
  "data": {}
}
```
**Status Codes**:
- 200: Successful request
- 400: Invalid parameters
- 401: Authentication required
- 403: Insufficient permissions

## Health Check API

### Comprehensive Health Check
**Endpoint**: `GET /api/health/`
**Description**: Get comprehensive health status of the system
**Response**:
```json
{
  "status": "healthy|unhealthy",
  "checks": {
    "database": {
      "status": "healthy|unhealthy",
      "message": "string"
    },
    "cache": {
      "status": "healthy|unhealthy",
      "message": "string"
    }
  },
  "timestamp": "datetime"
}
```
**Status Codes**:
- 200: System is healthy
- 503: System is unhealthy

### Simple Health Check
**Endpoint**: `GET /api/health/simple/`
**Description**: Simple health check for uptime monitoring
**Response**:
```json
{
  "status": "ok"
}
```
**Status Codes**:
- 200: System is running