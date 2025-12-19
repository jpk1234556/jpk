# Vercel Deployment Guide

This guide explains how to deploy the frontend of the Property Management System to Vercel.

## Prerequisites

1. A Vercel account (https://vercel.com)
2. This GitHub repository connected to Vercel

## Deploying Frontend to Vercel

### 1. Import Your Project

1. Log in to your Vercel dashboard
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository and click "Import"

### 2. Configure Project Settings

During the import process, configure the following settings:

- **Project Name**: `property-management-frontend`
- **Framework Preset**: `Other`
- **Root Directory**: `/frontend`
- **Build Command**: (Leave empty - this is a static site)
- **Output Directory**: `/`

### 3. Environment Variables

For the frontend, you may need to set environment variables depending on your configuration. Add any required environment variables in the "Environment Variables" section:

```
API_BASE_URL=https://your-backend-url.onrender.com
```

### 4. Deploy

Click "Deploy" to start the deployment process.

## Custom Domain (Optional)

To use a custom domain:

1. Go to your project dashboard
2. Click "Settings"
3. Navigate to "Domains"
4. Add your custom domain
5. Follow the DNS configuration instructions

## Environment-Specific Configuration

### Development

For local development, you can serve the frontend using any static file server or by opening the HTML files directly in your browser.

### Production

Vercel automatically optimizes your static files for production, including:

- Global CDN distribution
- Automatic HTTPS
- Compression
- Caching headers

## Connecting to Backend

Ensure your frontend can communicate with your backend by:

1. Setting the correct API base URL in your frontend code
2. Configuring CORS settings on your backend to allow requests from your Vercel domain
3. Using environment variables to manage different URLs for development and production

Example JavaScript API client configuration:

```javascript
// In your frontend JavaScript code
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

async function apiCall(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}/api${endpoint}`, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    });
    
    return response.json();
}
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend CORS settings allow requests from your Vercel domain.

2. **API Connection Issues**: Verify that your `API_BASE_URL` is correctly set and that your backend is accessible.

3. **Static Assets Not Loading**: Check that all asset paths are relative or correctly configured.

### Logs

Check the deployment logs in your Vercel dashboard:

1. Go to your project dashboard
2. Click "Deployments"
3. Select the deployment you want to inspect
4. Review the build logs and function logs

## Redeploying

To redeploy your frontend:

1. Push changes to your GitHub repository
2. Vercel will automatically detect changes and start a new deployment
3. Alternatively, you can trigger a manual deployment from the Vercel dashboard:
   - Go to your project dashboard
   - Click "Redeploy"
   - Select the deployment you want to redeploy or create a new one

## Preview Deployments

Vercel automatically creates preview deployments for pull requests:

1. Create a pull request with your changes
2. Vercel will automatically deploy a preview version
3. Test your changes before merging to the main branch

## Performance Optimization

Vercel automatically applies several optimizations:

- Image optimization
- Smart bundling
- Edge caching
- Global CDN distribution

For additional optimization, consider:

1. Minifying CSS and JavaScript files
2. Optimizing images
3. Using efficient API calls
4. Implementing proper caching strategies