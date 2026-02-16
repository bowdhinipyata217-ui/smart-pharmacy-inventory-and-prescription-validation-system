# Deployment Guide

This guide covers deploying the Pharmacy AI application to production.

## Pre-Deployment Checklist

- [ ] Change `SECRET_KEY` in `.env` to a secure random value
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up production database (MySQL)
- [ ] Configure production media/static file storage
- [ ] Set up SSL/TLS certificates
- [ ] Configure environment variables
- [ ] Set up backup strategy
- [ ] Configure logging
- [ ] Set up monitoring

## Production Settings

### Environment Variables

Update your `.env` file for production:

```env
SECRET_KEY=your-very-secure-secret-key-here-generate-with-openssl
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=pharmacy_ai_prod
DB_USER=pharmacy_user
DB_PASSWORD=secure-database-password
DB_HOST=localhost
DB_PORT=3306

# API Keys
OPENAI_API_KEY=your-openai-api-key
GOOGLE_VISION_API_KEY=your-google-vision-key

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment Options

### Option 1: Deploy with Gunicorn + Nginx

#### 1. Install Gunicorn

```bash
pip install gunicorn
```

#### 2. Create Gunicorn Service

Create `/etc/systemd/system/pharmacy-ai.service`:

```ini
[Unit]
Description=Pharmacy AI Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/pharmacy_ai
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/path/to/pharmacy_ai/pharmacy_ai.sock \
    pharmacy_ai.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 3. Configure Nginx

Create `/etc/nginx/sites-available/pharmacy-ai`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /path/to/pharmacy_ai/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/pharmacy_ai/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/pharmacy_ai/pharmacy_ai.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/pharmacy-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Start Gunicorn Service

```bash
sudo systemctl start pharmacy-ai
sudo systemctl enable pharmacy-ai
```

### Option 2: Deploy with Docker

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pharmacy_ai.wsgi:application"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: pharmacy_ai
      MYSQL_USER: pharmacy_user
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

Deploy:
```bash
docker-compose up -d
```

### Option 3: Deploy to Cloud Platforms

#### Heroku

1. Create `Procfile`:
```
web: gunicorn pharmacy_ai.wsgi:application
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create pharmacy-ai-app
heroku addons:create cleardb:ignite
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

#### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init
eb create pharmacy-ai-env
eb deploy
```

#### DigitalOcean App Platform

1. Create `app.yaml`:
```yaml
name: pharmacy-ai
services:
- name: web
  source_dir: /
  github:
    repo: your-repo
    branch: main
  run_command: gunicorn pharmacy_ai.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-secret-key
  - key: DEBUG
    value: "False"
```

## Database Setup

### Production MySQL Configuration

```sql
CREATE DATABASE pharmacy_ai_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pharmacy_user'@'localhost' IDENTIFIED BY 'secure-password';
GRANT ALL PRIVILEGES ON pharmacy_ai_prod.* TO 'pharmacy_user'@'localhost';
FLUSH PRIVILEGES;
```

### Run Migrations

```bash
python manage.py migrate
```

## Static Files

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Configure Static File Serving

For production, use a CDN or configure your web server to serve static files directly.

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database backups
- [ ] Rate limiting (consider django-ratelimit)
- [ ] CSRF protection enabled
- [ ] XSS protection enabled

## Monitoring & Logging

### Configure Logging

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/path/to/logs/pharmacy_ai.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Health Check Endpoint

Add to `urls.py`:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns += [path('health/', health_check)]
```

## Backup Strategy

### Database Backup Script

Create `backup_db.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u pharmacy_user -p pharmacy_ai_prod > backups/db_backup_$DATE.sql
```

### Automated Backups

Set up cron job:
```bash
0 2 * * * /path/to/backup_db.sh
```

## Performance Optimization

1. **Enable Caching**: Use Redis or Memcached
2. **Database Indexing**: Ensure proper indexes on frequently queried fields
3. **CDN**: Use CDN for static files
4. **Database Connection Pooling**: Configure MySQL connection pooling
5. **Gzip Compression**: Enable in Nginx
6. **Image Optimization**: Compress uploaded images

## Troubleshooting

### Check Logs

```bash
# Application logs
tail -f /path/to/logs/pharmacy_ai.log

# Nginx logs
tail -f /var/log/nginx/error.log

# Gunicorn logs
journalctl -u pharmacy-ai -f
```

### Common Issues

1. **Static files not loading**: Run `collectstatic`
2. **Database connection errors**: Check MySQL service and credentials
3. **Permission errors**: Check file permissions on media/static directories
4. **502 Bad Gateway**: Check Gunicorn service status

## Post-Deployment

1. Test all functionality
2. Monitor error logs
3. Set up alerts for critical errors
4. Schedule regular backups
5. Monitor performance metrics
6. Keep dependencies updated
