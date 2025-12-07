# Deployment Guide

## Production Deployment

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL (recommended for production)
- Redis (optional, for session storage)
- Web server (Nginx/Apache)
- WSGI server (Gunicorn/uWSGI)
- SSL certificate (Let's Encrypt)

---

## Step 1: Server Setup

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Dependencies
```bash
# Python and build tools
sudo apt install python3 python3-pip python3-venv -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Redis
sudo apt install redis-server -y

# Nginx
sudo apt install nginx -y
```

---

## Step 2: Database Configuration

### PostgreSQL Setup
```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE auth_service;
CREATE USER auth_user WITH PASSWORD 'your_secure_password';
ALTER ROLE auth_user SET client_encoding TO 'utf8';
ALTER ROLE auth_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE auth_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE auth_service TO auth_user;
\q
```

---

## Step 3: Application Setup

### Clone Repository
```bash
cd /opt
sudo mkdir auth-service
sudo chown $USER:$USER auth-service
cd auth-service
git clone https://github.com/Vishnu-Singh/authentication-services.git .
```

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

---

## Step 4: Environment Configuration

### Create Production .env File
```bash
cp .env.example .env
nano .env
```

### Update .env with Production Values
```bash
# Django Settings
DEBUG=False
SECRET_KEY=generate_a_long_random_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=auth_service
DATABASE_USER=auth_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Security
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password
```

### Update settings.py for Production
```python
# Add at the top
import os
from pathlib import Path

# Read environment variables
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DATABASE_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DATABASE_USER', ''),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DATABASE_HOST', ''),
        'PORT': os.getenv('DATABASE_PORT', ''),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Security settings
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
```

---

## Step 5: Database Migration

```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## Step 6: Gunicorn Configuration

### Create Gunicorn Socket
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/auth-service
ExecStart=/opt/auth-service/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          auth_service.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start Gunicorn
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

---

## Step 7: Nginx Configuration

### Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/auth-service
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Static files
    location /static/ {
        alias /opt/auth-service/staticfiles/;
    }
    
    # Media files (if any)
    location /media/ {
        alias /opt/auth-service/media/;
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/auth-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Step 8: SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Step 9: Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## Step 10: Monitoring & Logging

### Setup Log Rotation
```bash
sudo nano /etc/logrotate.d/auth-service
```

```
/opt/auth-service/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### Monitor Services
```bash
# Check Gunicorn
sudo systemctl status gunicorn

# Check Nginx
sudo systemctl status nginx

# View logs
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
```

---

## Docker Deployment (Alternative)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "auth_service.wsgi:application"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: auth_service
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: your_password

  redis:
    image: redis:7-alpine

  web:
    build: .
    command: gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Deploy with Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Maintenance

### Update Application
```bash
cd /opt/auth-service
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Backup Database
```bash
# PostgreSQL
pg_dump -U auth_user auth_service > backup_$(date +%Y%m%d).sql

# Restore
psql -U auth_user auth_service < backup_20251206.sql
```

### Monitor Performance
```bash
# Check system resources
htop

# Database connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Nginx status
curl http://localhost/nginx_status
```

---

## Security Checklist

- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Use strong database passwords
- [ ] Enable firewall
- [ ] Setup fail2ban
- [ ] Configure rate limiting
- [ ] Regular security updates
- [ ] Monitor authentication logs
- [ ] Setup backup strategy
- [ ] Configure monitoring/alerting

---

## Troubleshooting

### Gunicorn won't start
```bash
sudo journalctl -u gunicorn -n 50
```

### Nginx 502 Bad Gateway
```bash
# Check socket
ls -la /run/gunicorn.sock
# Check permissions
sudo chown www-data:www-data /run/gunicorn.sock
```

### Database connection errors
```bash
# Test connection
psql -U auth_user -h localhost auth_service
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```
