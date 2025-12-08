# Using Enhanced Features

This guide explains how to use the newly implemented features in the Property Management System.

## Email Notifications

### Setup
1. Configure email settings in the `.env` file:
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   DEFAULT_FROM_EMAIL=noreply@propertymanagement.com
   ADMIN_EMAIL=admin@propertymanagement.com
   ```

2. For Gmail, enable 2-factor authentication and generate an App Password.

### How Notifications Work
- **User Registration**: Admins receive email when new users register
- **User Approval**: Users receive email when their accounts are approved
- **Rent Due**: Tenants receive reminders before rent is due
- **Maintenance Requests**: Property managers receive alerts for new requests
- **Payments**: Tenants receive confirmations when payments are recorded

### Running Notifications Manually
```bash
# Send all types of notifications
python manage.py send_notifications

# Send specific notification types
python manage.py send_notifications --notification-type rent_due
python manage.py send_notifications --notification-type maintenance
python manage.py send_notifications --notification-type lease_expiry
```

## Search and Filtering

### Admin Module

#### Property Owners Page
- Use the search box to find owners by name or email
- Filter by approval status (Approved/Pending)
- Click "Clear Filters" to reset all filters

#### Properties Page
- Search properties by name
- Filter by property type (Hostel, Apartment, Hotel, Rental)
- Filter by property owner
- Click "Clear Filters" to reset all filters

#### Reports Page
- Select report type (Revenue, Occupancy, Maintenance, Tenants)
- Set date range using start and end date pickers
- Filter by specific property
- Click "Generate Report" to apply filters

### Property Owner Module

#### Tenants Page
- Search tenants by name, email, or phone
- Filter by status (Active/Expired)
- Filter by property
- Click "Clear Filters" to reset all filters

#### Payments Page
- Search payments by tenant name or property
- Filter by payment status (Paid, Pending, Overdue)
- Filter by property
- Click "Clear Filters" to reset all filters

#### Reports Page
- Select report type (Income, Occupancy, Maintenance, Tenants)
- Set date range using start and end date pickers
- Filter by specific property
- Click "Generate Report" to apply filters

## Responsive Design

### Mobile Usage
The application automatically adapts to different screen sizes:

- **Desktop (>1024px)**: Full layout with sidebar navigation
- **Tablet (768px-1024px)**: Adjusted layouts with flexible grids
- **Mobile (<768px)**: Stacked layouts with touch-friendly controls

### Features on Mobile
- Navigation menu converts to horizontal layout
- Forms adjust to full screen width
- Tables become horizontally scrollable
- Buttons resize for easier tapping
- Font sizes optimize for readability

## Data Export

### Admin Reports
- Navigate to Admin → Reports
- Select report type and filters
- Click "Export to CSV" to download data

### Property Owner Reports
- Navigate to Reports in Property Owner module
- Select report type and filters
- Click "Export to CSV" to download data

## Best Practices

### Email Notifications
- Test email configuration with the management commands
- Monitor logs for delivery failures
- Regularly verify that notification templates are up to date

### Search and Filtering
- Use specific search terms for better results
- Combine multiple filters for precise data views
- Clear filters periodically to avoid confusion

### Mobile Usage
- Test critical workflows on actual mobile devices
- Ensure all forms are usable on small screens
- Verify that touch targets are appropriately sized

## Troubleshooting

### Email Issues
- Check that all email settings are correctly configured
- Verify that the email account credentials are valid
- Review application logs for error messages
- Test with a simple email sending command

### Search Problems
- Ensure search terms are spelled correctly
- Try clearing filters and searching again
- Check browser console for JavaScript errors

### Mobile Display Issues
- Refresh the page to ensure latest CSS is loaded
- Clear browser cache if changes don't appear
- Check that viewport meta tag is present in HTML

## Feedback
If you encounter any issues with these enhanced features, please report them with:
- Description of the problem
- Steps to reproduce
- Browser/device information
- Screenshots if applicable