# Email Notifications System

The Property Management System includes a comprehensive email notification system that automatically sends notifications for key events in the application.

## Features

1. **User Registration Notifications** - Notifies administrators when new users register
2. **User Approval Notifications** - Notifies users when their accounts are approved
3. **Rent Due Notifications** - Reminds tenants when rent payments are due
4. **Maintenance Request Notifications** - Alerts property managers about new maintenance requests
5. **Payment Received Notifications** - Confirms to tenants when payments are received

## Configuration

To enable email notifications, you need to configure the email settings in the `.env` file:

```env
# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@propertymanagement.com
ADMIN_EMAIL=admin@propertymanagement.com
FRONTEND_BASE_URL=http://localhost:3000
```

### Gmail Configuration

If using Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this app password as the EMAIL_HOST_PASSWORD

## Notification Types

### User Registration
Sent to administrators when a new user registers in the system.

### User Approval
Sent to users when their account is approved by an administrator.

### Rent Due
Sent to tenants when rent payments are due (configurable number of days in advance).

### Maintenance Requests
Sent to property managers when new maintenance requests are submitted.

### Payment Received
Sent to tenants when their payments are recorded in the system.

## Running Notifications Manually

You can manually trigger notifications using Django management commands:

```bash
# Send all types of notifications
python manage.py send_notifications

# Send only rent due notifications
python manage.py send_notifications --notification-type rent_due

# Send rent due notifications 7 days in advance
python manage.py send_notifications --notification-type rent_due --days-before-due 7

# Send only lease expiry notifications
python manage.py send_notifications --notification-type lease_expiry

# Send only maintenance notifications
python manage.py send_notifications --notification-type maintenance
```

## Scheduling Notifications

For production use, schedule the notification commands to run automatically:

### Using Cron (Linux/Mac)

Add to crontab (`crontab -e`):

```bash
# Send rent due notifications daily at 9 AM
0 9 * * * cd /path/to/project && python manage.py send_notifications --notification-type rent_due

# Send lease expiry notifications daily at 10 AM
0 10 * * * cd /path/to/project && python manage.py send_notifications --notification-type lease_expiry

# Send maintenance notifications every hour
0 * * * * cd /path/to/project && python manage.py send_notifications --notification-type maintenance
```

### Using Windows Task Scheduler

1. Create a batch file to run the command
2. Schedule it using Windows Task Scheduler

## Disabling Notifications

To disable email notifications, simply remove or comment out the email configuration in the `.env` file. The system will log warnings but continue to function normally.

## Customization

Email templates can be customized by modifying the HTML files in the `templates/emails/` directory:

- `new_user_registration.html` - New user registration emails
- `user_approved.html` - User approval emails
- `rent_due.html` - Rent due notification emails
- `maintenance_request.html` - Maintenance request emails
- `payment_received.html` - Payment received confirmation emails

## Troubleshooting

### Emails Not Sending

1. Check that all email settings are correctly configured in `.env`
2. Verify that the email account credentials are correct
3. Ensure that the email provider allows SMTP access
4. Check the application logs for error messages

### SSL/TLS Issues

If you encounter SSL/TLS connection issues:
1. Try setting `EMAIL_USE_TLS=False` and `EMAIL_PORT=25`
2. Or try `EMAIL_USE_SSL=True` and `EMAIL_PORT=465`

### Gmail Authentication Issues

1. Ensure 2-factor authentication is enabled
2. Use an App Password instead of your regular password
3. Check that "Less secure app access" is not required (it usually is not with App Passwords)