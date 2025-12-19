# Property Management System Production Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Deployment Options](#deployment-options)
4. [Step-by-Step Deployment](#step-by-step-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Security Configuration](#security-configuration)
8. [Performance Optimization](#performance-optimization)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Backup and Recovery](#backup-and-recovery)
11. [Scaling Considerations](#scaling-considerations)
12. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04 LTS or newer), macOS 10.15+, or Windows Server 2019+
- **Python**: 3.8 or newer
- **Database**: PostgreSQL 12+ or compatible database service
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: Minimum 20GB SSD storage (50GB recommended)
- **Network**: Stable internet connection with outbound access

### Software Dependencies
- Python 3.8+
- PostgreSQL 12+
- Redis 6.0+
- Nginx or Apache (for reverse proxy)
- SSL certificate (Let's Encrypt recommended)

### Services Required
- Email service (SMTP provider or AWS SES, SendGrid, etc.)
- SMS service (Twilio, AWS SNS, etc. - optional)
- Cloud storage (AWS S3, Google Cloud Storage, etc. - optional)

## Architecture Overview

### Components
1. **Web Application Server**: Django application running with Gunicorn
2. **Database**: PostgreSQL for data persistence
3. **Cache**: Redis for caching and session storage
4. **Reverse Proxy**: Nginx for SSL termination and static file serving
5. **Task Queue**: Celery for background tasks (optional)
6. **Monitoring**: Sentry for error tracking, custom logging

### Data Flow
```
Client → SSL Termination (Nginx) → Django Application (Gunicorn) 
  ↓
Database (PostgreSQL) ←→ Cache (Redis) ←→ Background Tasks (Celery)
```

## Deployment Options

### Option 1: Cloud Platform (Recommended)
- **Platform**: Render, Heroku, AWS, Google Cloud, Azure
- **Pros**: Easy scaling, managed services, built-in monitoring
- **Cons**: Higher cost, less control

### Option 2: Virtual Private Server (VPS)
- **Providers**: DigitalOcean, Linode, Vultr, AWS EC2
- **Pros**: Cost-effective, full control
- **Cons**: Requires sysadmin skills, manual maintenance

### Option 3: Dedicated Server
- **Providers**: Own hardware or colocation
- **Pros**: Maximum performance and control
- **Cons**: Highest cost and maintenance burden

## Step-by-Step Deployment

### 1. Server Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server git -y

# Create application user
sudo adduser --disabled-password --gecos "" propertymanager
```

### 2. Application Installation
```bash
# Switch to application user
sudo su - propertymanager

# Clone repository
git clone https://github.com/your-username/property-management-system.git
cd property-management-system/backend/property_management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Switch to postgres user
sudo su - postgres

# Create database and user
psql -c "CREATE DATABASE property_management;"
psql -c "CREATE USER pm_user WITH PASSWORD 'secure_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE property_management TO pm_user;"
psql -c "ALTER USER pm_user CREATEDB;"
exit

# Run migrations
cd /home/propertymanager/property-management-system/backend/property_management
source venv/bin/activate
python manage.py migrate --settings=config.production_settings
```

### 4. Environment Configuration
Create `.env.production` file:
```bash
# Django Settings
SECRET_KEY=your-very-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1

# Database Settings
DATABASE_URL=postgresql://pm_user:secure_password@localhost:5432/property_management

# Redis Settings
REDIS_URL=redis://localhost:6379/1

# Email Settings
EMAIL_HOST=your-smtp-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
FRONTEND_BASE_URL=https://yourdomain.com

# CORS Settings
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Sentry Settings (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=1.0
```

### 5. Static Files Collection
```bash
python manage.py collectstatic --settings=config.production_settings --noinput
```

### 6. Gunicorn Configuration
Create `/etc/systemd/system/property-management.service`:
```ini
[Unit]
Description=Property Management System
After=network.target

[Service]
User=propertymanager
Group=www-data
WorkingDirectory=/home/propertymanager/property-management-system/backend/property_management
ExecStart=/home/propertymanager/property-management-system/backend/property_management/venv/bin/gunicorn --workers 3 --bind unix:/run/property-management.sock config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start property-management
sudo systemctl enable property-management
```

### 7. Nginx Configuration
Create `/etc/nginx/sites-available/property-management`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://unix:/run/property-management.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/propertymanager/property-management-system/backend/property_management/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/propertymanager/property-management-system/backend/property_management/media/;
        expires 1d;
    }
}
```

Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/property-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Final Setup
```bash
# Create superuser
python manage.py createsuperuser --settings=config.production_settings

# Start Redis if not already running
sudo systemctl start redis

# Restart all services
sudo systemctl restart property-management
sudo systemctl restart nginx
```

## Environment Configuration

### Production Environment Variables
The production environment requires the following variables in `.env.production`:

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Django secret key | Yes |
| DEBUG | Debug mode (should be False) | Yes |
| ALLOWED_HOSTS | Comma-separated list of allowed domains | Yes |
| DATABASE_URL | PostgreSQL connection URL | Yes |
| REDIS_URL | Redis connection URL | Yes |
| EMAIL_HOST | SMTP server hostname | Yes |
| EMAIL_PORT | SMTP server port | Yes |
| EMAIL_USE_TLS | Use TLS for SMTP | Yes |
| EMAIL_HOST_USER | SMTP username | Yes |
| EMAIL_HOST_PASSWORD | SMTP password | Yes |
| DEFAULT_FROM_EMAIL | Default sender email | Yes |
| ADMIN_EMAIL | Administrator email | Yes |
| FRONTEND_BASE_URL | Frontend application URL | Yes |
| CORS_ALLOWED_ORIGINS | Comma-separated list of allowed origins | Yes |
| SENTRY_DSN | Sentry DSN for error tracking | No |
| SENTRY_ENVIRONMENT | Sentry environment name | No |

### Security Settings
Additional security settings are automatically applied in production:
- SSL redirect enabled
- HSTS headers set
- Content type sniffing disabled
- XSS protection enabled
- Frame embedding disabled
- Secure cookies enabled

## Database Setup

### PostgreSQL Configuration
For optimal performance, adjust these PostgreSQL settings in `postgresql.conf`:

```conf
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB

# Connection settings
max_connections = 100
superuser_reserved_connections = 3

# Checkpoint settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB

# Query planner
random_page_cost = 1.1
effective_io_concurrency = 200
```

### Database Backup Strategy
```bash
# Daily backup script
#!/bin/bash
pg_dump -U pm_user -h localhost property_management > /backups/pm_backup_$(date +%Y%m%d_%H%M%S).sql

# Weekly cleanup
find /backups -name "pm_backup_*.sql" -mtime +7 -delete
```

Schedule with cron:
```bash
# Daily at 2 AM
0 2 * * * /home/propertymanager/scripts/backup_db.sh

# Weekly cleanup on Sundays at 3 AM
0 3 * * 0 find /backups -name "pm_backup_*.sql" -mtime +7 -delete
```

## Security Configuration

### Firewall Setup
```bash
# UFW firewall configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Fail2Ban Configuration
Install and configure Fail2Ban for brute force protection:
```bash
sudo apt install fail2ban -y

# Create jail.local
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Add custom rules for Django
echo "[django-admin]
enabled = true
port = http,https
filter = django-admin
logpath = /var/log/nginx/access.log
maxretry = 3
bantime = 3600" | sudo tee -a /etc/fail2ban/jail.local
```

### Application-Level Security
- Rate limiting implemented for API endpoints
- Password strength requirements enforced
- Session timeouts configured
- CSRF protection enabled
- SQL injection prevention through Django ORM
- XSS prevention through template escaping

## Performance Optimization

### Gunicorn Tuning
Adjust Gunicorn worker settings based on server resources:
```bash
# For servers with 4GB RAM
--workers 3 --worker-class sync --worker-connections 1000

# For servers with 8GB+ RAM
--workers 4 --worker-class gevent --worker-connections 1000
```

### Database Indexes
Key database indexes are automatically created for:
- User authentication fields
- Property ownership relationships
- Tenant lease dates
- Payment timestamps
- Maintenance request priorities

### Caching Strategy
Redis is used for:
- Session storage
- API response caching
- Dashboard statistics caching
- Report data caching

Configure cache timeouts in `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
        'TIMEOUT': 300,  # 5 minutes default
        'OPTIONS': {
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 20,
                'retry_on_timeout': True,
            }
        }
    }
}
```

### Static File Optimization
- WhiteNoise serves compressed static files
- Long-term caching headers for static assets
- Automatic manifest generation for cache busting

## Monitoring and Logging

### Log Files Location
- Application logs: `/var/log/property-management/`
- Nginx logs: `/var/log/nginx/`
- PostgreSQL logs: `/var/log/postgresql/`
- System logs: `/var/log/syslog`

### Log Rotation
Configure logrotate for application logs:
```bash
# /etc/logrotate.d/property-management
/var/log/property-management/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 propertymanager propertymanager
    postrotate
        systemctl reload property-management
    endscript
}
```

### Health Checks
Monitor these endpoints:
- `/api/health/` - Comprehensive health check
- `/api/health/simple/` - Lightweight health check

### Performance Monitoring
- Sentry integration for error tracking
- Custom performance logging
- Database query performance monitoring
- Cache hit/miss ratio tracking

## Backup and Recovery

### Automated Backup Strategy
Three-tier backup approach:

1. **Hourly Database Snapshots**
   - Transaction log backups
   - Point-in-time recovery capability

2. **Daily Full Backups**
   - Complete database dumps
   - Application code snapshots
   - Configuration backups

3. **Weekly Offsite Backups**
   - Encrypted cloud storage
   - Geographic redundancy
   - Long-term retention

### Recovery Procedures

#### Database Recovery
```bash
# Restore from backup
pg_restore -U pm_user -h localhost -d property_management backup_file.dump

# Point-in-time recovery
pg_rewind --target-pgdata=/var/lib/postgresql/data \
          --source-server='host=localhost port=5432 dbname=property_management' \
          --restore-target-time='2023-01-01 12:00:00'
```

#### Application Recovery
```bash
# Rollback to previous version
git checkout v1.2.3
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=config.production_settings
sudo systemctl restart property-management
```

### Disaster Recovery Plan
1. **Immediate Response** (0-4 hours)
   - Identify failure point
   - Activate backup systems
   - Notify stakeholders

2. **Short-term Recovery** (4-24 hours)
   - Restore from latest backup
   - Validate data integrity
   - Resume operations

3. **Long-term Recovery** (1-7 days)
   - Root cause analysis
   - Implement preventive measures
   - Update disaster recovery documentation

## Scaling Considerations

### Horizontal Scaling
For high-traffic deployments:

1. **Load Balancer**
   - Distribute traffic across multiple application servers
   - Health checks for automatic failover
   - SSL termination at load balancer

2. **Database Replication**
   - Master-slave replication
   - Read replicas for reporting queries
   - Automatic failover configuration

3. **Caching Layer**
   - Distributed Redis cluster
   - Session sharing across servers
   - Cache warming strategies

### Vertical Scaling
Upgrade server resources:
- Increase CPU cores
- Add more RAM
- Upgrade to SSD storage
- Expand network bandwidth

### Microservices Architecture
For very large deployments, consider splitting services:
- User management service
- Property management service
- Payment processing service
- Notification service

## Troubleshooting

### Common Issues and Solutions

#### Application Won't Start
1. Check Gunicorn logs: `journalctl -u property-management -f`
2. Verify environment variables: `cat .env.production`
3. Check database connectivity: `psql -U pm_user -d property_management`
4. Validate Python dependencies: `pip check`

#### Database Connection Errors
1. Verify PostgreSQL is running: `sudo systemctl status postgresql`
2. Check database credentials in `.env.production`
3. Ensure PostgreSQL accepts connections: `netstat -tlnp | grep 5432`
4. Review PostgreSQL logs: `/var/log/postgresql/postgresql-*.log`

#### Performance Issues
1. Monitor system resources: `htop`, `iotop`
2. Check database query performance: `EXPLAIN ANALYZE`
3. Review application logs for slow requests
4. Analyze cache hit ratios in Redis

#### SSL Certificate Problems
1. Verify certificate validity: `openssl x509 -in /path/to/cert.pem -text -noout`
2. Check certificate expiration: `certbot certificates`
3. Renew certificates if needed: `sudo certbot renew`
4. Verify Nginx SSL configuration

#### Email Delivery Failures
1. Check SMTP server settings in `.env.production`
2. Verify email credentials
3. Test email delivery manually
4. Review email service provider status

### Emergency Procedures

#### Complete System Failure
1. **Immediate Actions**
   - Check system status: `systemctl status`
   - Review recent logs: `journalctl -f`
   - Assess damage scope

2. **Recovery Steps**
   - Restore from latest backup
   - Validate restored data
   - Bring services online gradually
   - Monitor for issues

#### Security Breach
1. **Containment**
   - Isolate affected systems
   - Change all passwords
   - Revoke compromised credentials

2. **Investigation**
   - Review access logs
   - Analyze system changes
   - Identify breach vector

3. **Remediation**
   - Patch vulnerabilities
   - Implement additional security measures
   - Conduct security audit

### Support Resources

#### Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [Admin User Manual](ADMIN_USER_MANUAL.md)
- [Property Owner User Manual](PROPERTY_OWNER_USER_MANUAL.md)
- [Error Handling Guide](ERROR_HANDLING_MONITORING.md)

#### Community Support
- GitHub Issues: https://github.com/your-username/property-management-system/issues
- Stack Overflow: Tag with "property-management-system"
- Discord Community: [link to community]

#### Professional Support
- Enterprise support plans available
- SLA guarantees for response times
- Dedicated support engineers