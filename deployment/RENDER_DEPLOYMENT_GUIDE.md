# Render Deployment Guide

This guide explains how to deploy the Property Management System to Render.

## Prerequisites

1. A Render account (https://render.com)
2. A PostgreSQL database (can be provisioned on Render)
3. This GitHub repository connected to Render

## Deploying to Render

### 1. Create a PostgreSQL Database on Render

1. Log in to your Render dashboard
2. Click "New +" and select "PostgreSQL"
3. Choose a name for your database (e.g., `property-management-db`)
4. Select the free tier or a paid tier based on your needs
5. Click "Create Database"
6. Once created, note the `External Database URL` - you'll need this for the web service

### 2. Deploy the Web Service

1. Log in to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the following settings:
   - **Name**: `property-management-backend`
   - **Region**: Choose your preferred region
   - **Branch**: `main` (or your preferred branch)
   - **Root Directory**: `backend/property_management`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Configure Environment Variables

In the "Advanced" section of your web service configuration, add the following environment variables:

```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=your-postgresql-database-url
EMAIL_HOST=your-email-host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 4. Deploy

Click "Create Web Service" to start the deployment process.

## Setting Up the Database

After your web service is created:

1. Go to your web service dashboard
2. Click "Manual Deploy" and select "Clear build cache & deploy"
3. Once deployed, open the "Shell" tab
4. Run the following commands to set up your database:

```bash
python manage.py migrate --settings=config.production_settings
python manage.py createsuperuser --settings=config.production_settings
```

## Deploying Frontend to Vercel

For deploying the frontend to Vercel:

1. Create a new project on Vercel
2. Connect your GitHub repository
3. Set the root directory to `/frontend`
4. No build command is needed for static sites
5. Set the output directory to `/`
6. Add environment variables if needed

## Environment-Specific Configuration

### Production Settings

The application uses `config.production_settings` for production environments. This configuration includes:

- Security enhancements
- Database connection via `DATABASE_URL`
- Static file serving with WhiteNoise
- CORS configuration
- Email settings
- Logging configuration
- Cache configuration with Redis

### Development Settings

For local development, use the default settings in `config.settings`.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Ensure your `DATABASE_URL` is correctly set and the database is running.

2. **Static Files Not Loading**: Make sure WhiteNoise is properly configured in your middleware.

3. **CORS Errors**: Verify that `CORS_ALLOWED_ORIGINS` includes your frontend domain.

4. **Email Configuration**: Check that all email environment variables are correctly set.

### Logs

Check the logs in your Render dashboard for any deployment or runtime errors:

1. Go to your web service dashboard
2. Click the "Logs" tab
3. Review recent log entries for errors

## Scaling

Render automatically scales your application based on traffic. For more control:

1. Go to your web service dashboard
2. Click "Settings"
3. Adjust the instance count and type as needed

## Updating Your Application

To update your deployed application:

1. Push changes to your GitHub repository
2. Render will automatically detect changes and start a new deployment
3. Alternatively, you can trigger a manual deployment from the Render dashboard