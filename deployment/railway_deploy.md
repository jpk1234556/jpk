# Railway Deployment Guide

## Prerequisites

1. Create a Railway account: https://railway.app/
2. Install Railway CLI (optional): https://docs.railway.app/develop/cli

## Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
# Make sure your code is in a Git repository
git init
git add .
git commit -m "Initial commit for Railway deployment"

# Push to GitHub (recommended)
git remote add origin https://github.com/yourusername/property-management-system.git
git push -u origin main
```

### 2. Deploy via Railway Dashboard

#### Option A: GitHub Integration (Recommended)

1. Go to https://railway.app/
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account
5. Select your property management repository
6. Railway will automatically detect it's a Django app

#### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Add PostgreSQL Database

1. In Railway dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway will automatically create DATABASE_URL environment variable

### 4. Configure Environment Variables

In Railway dashboard, go to your service → Variables tab:

```
SECRET_KEY=your-super-secret-key-here
DJANGO_SETTINGS_MODULE=config.production_settings
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourapp.com
FRONTEND_BASE_URL=https://your-app.railway.app
DEBUG=False
```

### 5. Configure Build Settings

In Railway dashboard, go to Settings → Build:

- **Build Command**: `cd backend/property_management && pip install -r ../../requirements.txt`
- **Start Command**: `cd backend/property_management && gunicorn config.wsgi --bind 0.0.0.0:$PORT`

### 6. Run Initial Setup

After deployment, use Railway CLI or dashboard console:

```bash
# Run migrations
railway run python backend/property_management/manage.py migrate

# Create admin user
railway run python backend/property_management/manage.py shell
# Then in shell:
# from django.contrib.auth import get_user_model
# User = get_user_model()
# User.objects.create_superuser('admin', 'admin@example.com', 'admin')
```

## Alternative: One-Click Deploy

Create a `railway.json` file in your project root:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend/property_management && gunicorn config.wsgi --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/api/health/"
  }
}
```

## Environment Variables

Set these in Railway dashboard:

```
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.production_settings
DATABASE_URL=postgresql://... (automatically set by Railway)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourapp.com
ADMIN_EMAIL=admin@yourapp.com
FRONTEND_BASE_URL=https://your-app.railway.app
DEBUG=False
```

## Post-Deployment

### Access Your App

- **Main App**: https://your-app.railway.app
- **Admin Interface**: https://your-app.railway.app/admin/
- **API**: https://your-app.railway.app/api/

### Monitor Logs

- View logs in Railway dashboard under "Deployments" tab
- Real-time logs available in the dashboard

## Custom Domain

1. Go to Settings → Domains in Railway dashboard
2. Add your custom domain
3. Configure DNS records as shown

## Advantages of Railway

- Automatic deployments from GitHub
- Built-in PostgreSQL
- Easy environment variable management
- Great developer experience
- Automatic SSL certificates
- Good performance and reliability
