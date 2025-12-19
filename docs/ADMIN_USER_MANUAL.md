# Admin User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Dashboard Overview](#dashboard-overview)
4. [User Management](#user-management)
5. [Property Management](#property-management)
6. [Reports](#reports)
7. [Settings](#settings)
8. [API Integration](#api-integration)
9. [Troubleshooting](#troubleshooting)

## Introduction

Welcome to the Property Management System Admin User Manual. This guide will help you navigate and utilize all the features available to administrators in the system.

As an admin, you have comprehensive access to all system features, including:
- Managing property owner accounts
- Approving new property owner registrations
- Overseeing all properties in the system
- Generating system-wide reports
- Configuring system settings

## Getting Started

### Login Process
1. Navigate to the admin login page
2. Enter your admin username and password
3. Click the "Login" button
4. You will be redirected to the admin dashboard

### Navigation
The admin interface consists of the following main sections:
- Dashboard: Overview of system statistics
- Users: Manage property owner accounts
- Properties: View all properties in the system
- Reports: Generate system-wide reports
- Settings: Configure system settings

## Dashboard Overview

The admin dashboard provides a quick overview of key system metrics:
- Total Property Owners: Number of registered property owners
- Total Properties: Number of properties in the system
- Pending Approvals: Number of property owner accounts awaiting approval
- Active Tenants: Total number of tenants across all properties

### Dashboard Refresh
- The dashboard automatically refreshes every 5 minutes
- Click the "Refresh" button to manually update the statistics
- Export dashboard data using the "Export Data" button

## User Management

### Viewing Users
To view all users in the system:
1. Click on the "Users" link in the navigation menu
2. You will see a list of all registered users with their details
3. Use the search bar to filter users by name or email
4. Sort columns by clicking on the column headers

### Approving Property Owners
To approve a new property owner:
1. Go to the Users page
2. Find the user you want to approve
3. Click the "Edit" button next to their name
4. Set the "Approved" status to "Yes"
5. Set the "Role" to "Property Owner"
6. Click "Save"

### Creating Users
To create a new user:
1. Go to the Users page
2. Click the "Add New User" button
3. Fill in the required information:
   - Username
   - Email address
   - Password
4. Set the user role (Admin or Property Owner)
5. Set approval status if needed
6. Click "Create User"

### Editing Users
To edit a user's information:
1. Go to the Users page
2. Find the user you want to edit
3. Click the "Edit" button next to their name
4. Make the necessary changes
5. Click "Save"

### Deleting Users
To delete a user:
1. Go to the Users page
2. Find the user you want to delete
3. Click the "Delete" button next to their name
4. Confirm the deletion when prompted
5. Note: This action cannot be undone

### Bulk Operations
- Select multiple users using checkboxes
- Perform bulk actions like approval or deletion
- Export user lists to CSV format

## Property Management

### Viewing Properties
To view all properties in the system:
1. Click on the "Properties" link in the navigation menu
2. You will see a list of all properties with their details
3. Filter properties by type or owner using the filter options
4. Sort properties by clicking on column headers

### Creating Properties
To create a new property:
1. Go to the Properties page
2. Click the "Add New Property" button
3. Fill in the required information:
   - Property Name
   - Property Type (Hostel, Apartment, Hotel, Rental)
   - Address
   - Owner (select from approved property owners)
4. Add property description and amenities (optional)
5. Click "Create Property"

### Editing Properties
To edit a property's information:
1. Go to the Properties page
2. Find the property you want to edit
3. Click the "Edit" button next to its name
4. Make the necessary changes
5. Click "Save"

### Deleting Properties
To delete a property:
1. Go to the Properties page
2. Find the property you want to delete
3. Click the "Delete" button next to its name
4. Confirm the deletion when prompted
5. Note: All units, tenants, and related data will also be deleted

### Property Details
- View property statistics including occupancy rates
- See maintenance requests for the property
- View payment history for the property
- Access property documents and photos

## Reports

The system provides several types of reports for administrators:

### Revenue Report
Shows financial data including:
- Total revenue over a specified period
- Revenue broken down by property
- Monthly revenue trends
- Outstanding payments

To generate a revenue report:
1. Click on the "Reports" link in the navigation menu
2. Select "Revenue" from the report type dropdown
3. Optionally specify a date range
4. Optionally select specific properties
5. Click "Generate Report"
6. Export the report to PDF or CSV using the export buttons

### Occupancy Report
Shows occupancy statistics including:
- Overall occupancy rate
- Occupancy by property
- Total units vs. occupied units
- Vacancy trends over time

To generate an occupancy report:
1. Click on the "Reports" link in the navigation menu
2. Select "Occupancy" from the report type dropdown
3. Optionally specify a date range
4. Click "Generate Report"

### Maintenance Report
Shows maintenance request statistics including:
- Total maintenance requests
- Requests by status (pending, in progress, completed)
- Requests by priority (low, medium, high)
- Average resolution time
- Recent maintenance requests

To generate a maintenance report:
1. Click on the "Reports" link in the navigation menu
2. Select "Maintenance" from the report type dropdown
3. Optionally specify a date range
4. Click "Generate Report"

### Tenant Report
Shows tenant-related statistics including:
- Total number of tenants
- Active vs. expired leases
- Tenant distribution by property
- Recent tenant registrations
- Tenant retention rates

To generate a tenant report:
1. Click on the "Reports" link in the navigation menu
2. Select "Tenants" from the report type dropdown
3. Optionally specify a date range
4. Click "Generate Report"

### Custom Reports
- Combine multiple report types
- Schedule automatic report generation
- Set up email delivery for reports
- Create report templates for regular use

## Settings

The settings section allows you to configure various system parameters:

### Company Information
- Company name
- Address
- Phone number
- Email address
- Logo upload

### Currency and Locale
- Currency type
- Timezone
- Date format
- Number format

### Property Settings
- Default lease term
- Grace period for rent payments
- Late fee calculation
- Notice period settings

### Notifications
- Enable/disable different types of notifications
- Notification frequency
- Notification email address
- SMS notification settings

### Security
- Minimum password length
- Password complexity requirements
- Session timeout duration
- Two-factor authentication settings
- Failed login attempt limits

### Integrations
- Payment gateway configuration
- Google Maps integration
- SMS service settings
- Cloud storage settings
- Email service configuration

To update settings:
1. Click on the "Settings" link in the navigation menu
2. Navigate to the appropriate settings section
3. Modify the desired settings
4. Click "Save Settings"

### Audit Trail
- View system configuration changes
- Track user activity
- Monitor security events
- Export audit logs

## API Integration

The Property Management System provides a comprehensive REST API for integration with external systems.

### Authentication
All API requests require authentication using token-based authentication:
1. Obtain an authentication token by logging in via the API
2. Include the token in the Authorization header: `Authorization: Token YOUR_TOKEN`

### Available Endpoints
Refer to the [API Documentation](API_DOCUMENTATION.md) for detailed information about all available endpoints:
- User Management API
- Property Management API
- Unit Management API
- Tenant Management API
- Maintenance Request API
- Payment Tracking API
- Admin Module API
- Property Owner Module API

### Rate Limiting
- 1000 requests per hour per user
- Exceeding limits will result in 429 (Too Many Requests) responses
- Check the `X-Rate-Limit-Remaining` header to monitor your usage

### Webhooks
- Configure webhook URLs for real-time notifications
- Supported events include:
  - New tenant registration
  - Payment received
  - Maintenance request created
  - Lease expiration warnings

### Data Export
- Export data in JSON, CSV, or XML formats
- Schedule automated exports
- Configure export filters and transformations

## Troubleshooting

### Common Issues

#### Login Problems
- Ensure you're using the correct username and password
- Check that your account has admin privileges
- Contact system support if you continue to have issues

#### Report Generation Issues
- Ensure date formats are correct (YYYY-MM-DD)
- Verify that the selected date range contains data
- Refresh the page and try again

#### User Approval Issues
- Ensure the user has completed registration
- Check that the user's email is verified (if applicable)
- Verify that you have the necessary permissions

#### Property Creation Issues
- Verify that all required fields are filled
- Ensure the selected owner is approved
- Check for duplicate property names

#### API Integration Issues
- Verify your authentication token is valid
- Check that you have the required permissions for the endpoint
- Review the API documentation for correct request format

### System Performance
- If the system is running slowly, try clearing your browser cache
- Close other browser tabs to free up memory
- Contact support if performance issues persist

### Contact Support
If you encounter issues not covered in this manual, please contact:
- Email: support@propertymanagement.com
- Phone: (555) 123-4567

For technical issues, please include:
- Description of the problem
- Steps to reproduce the issue
- Screenshots if applicable
- Browser and operating system information
- Error messages received