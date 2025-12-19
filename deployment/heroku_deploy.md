# Heroku Deployment Guide

## Prerequisites

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account: https://signup.heroku.com/

## Step-by-Step Deployment

### 1. Prepare Your Code

```bash
# Make sure you're in the project root directory
cd /path/to/your/property-management-system

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for deployment"
```

### 2. Create Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create your-property-management-app

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev
```

### 3. Set Environment Variables

```bash
# Set Django settings module for production
heroku config:set DJANGO_SETTINGS_MODULE=config.production_settings

# Set secret key (generate a new one for production)
heroku config:set SECRET_KEY="your-super-secret-key-here"

# Set email configuration (optional)
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
heroku config:set DEFAULT_FROM_EMAIL="noreply@yourapp.com"

# Set frontend URL
heroku config:set FRONTEND_BASE_URL="https://your-property-management-app.herokuapp.com"
```

### 4. Deploy to Heroku

```bash
# Deploy your code
git push heroku main

# Run database migrations
heroku run python backend/property_management/manage.py migrate

# Create admin user
heroku run python backend/property_management/manage.py shell
# In the shell, run:
# from django.contrib.auth import get_user_model
# User = get_user_model()
# User.objects.create_superuser('admin', 'admin@example.com', 'your-secure-password')

# Or use the automated script
heroku run "cd backend/property_management && echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')\" | python manage.py shell"
```

### 5. Open Your App

```bash
heroku open
```

## Environment Variables Needed

Set these in Heroku dashboard or via CLI:

```bash
# Required
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DJANGO_SETTINGS_MODULE="config.production_settings"

# Optional (Email)
heroku config:set EMAIL_HOST="smtp.gmail.com"
heroku config:set EMAIL_PORT="587"
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"
heroku config:set DEFAULT_FROM_EMAIL="noreply@yourapp.com"
heroku config:set ADMIN_EMAIL="admin@yourapp.com"

# Frontend URL
heroku config:set FRONTEND_BASE_URL="https://your-app-name.herokuapp.com"
```

## Post-Deployment

### Access Your App

- **Main App**: https://your-app-name.herokuapp.com
- **Admin Interface**: https://your-app-name.herokuapp.com/admin/
- **API**: https://your-app-name.herokuapp.com/api/

### Default Login

- Username: `admin`
- Password: `admin` (change this in production!)

## Troubleshooting

### View Logs

```bash
heroku logs --tail
```

### Run Commands

```bash
# Access Django shell
heroku run python backend/property_management/manage.py shell

# Run migrations
heroku run python backend/property_management/manage.py migrate

# Collect static files
heroku run python backend/property_management/manage.py collectstatic --noinput
```

### Common Issues

1. **Static Files Not Loading**

   ```bash
   heroku run python backend/property_management/manage.py collectstatic --noinput
   ```

2. **Database Connection Issues**

   - Check that PostgreSQL addon is added
   - Verify DATABASE_URL is set automatically

3. **Environment Variables**
   ```bash
   heroku config
   ```

## Scaling (Optional)

```bash
# Scale web dynos
heroku ps:scale web=1

# Upgrade database (if needed)
heroku addons:upgrade heroku-postgresql:standard-0
```

## Custom Domain (Optional)

```bash
# Add custom domain
heroku domains:add www.yourapp.com

# Configure DNS to point to Heroku
# Add CNAME record: www -> your-app-name.herokuapp.com
```
