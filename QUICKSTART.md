# Quick Start Guide

## 1. Initial Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

## 2. Start the Server

```bash
python manage.py runserver
```

Server will be available at: http://localhost:8000

## 3. Access Admin Panel

Visit: http://localhost:8000/admin/

Login with your superuser credentials to manage:
- Users
- API Keys
- OAuth Clients
- SAML Service Providers
- Routing Rules

## 4. Quick Test Examples

### Test Session Authentication

```bash
# Register a user
curl -X POST http://localhost:8000/api/auth/session/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/session/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }' \
  -c cookies.txt

# Check status
curl -X GET http://localhost:8000/api/auth/session/status/ \
  -b cookies.txt
```

### Test JWT Token

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Response will contain access and refresh tokens
# Use the access token for authenticated requests:

curl -X GET http://localhost:8000/api/auth/session/status/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Test API Key Creation

```bash
# First, get a JWT token (see above)
# Then create an API key:

curl -X POST http://localhost:8000/api/auth/token/api-key/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Test API Key"
  }'

# Use the API key:
curl -X GET http://localhost:8000/api/auth/token/api-key/verify/ \
  -H "X-API-Key: YOUR_API_KEY_HERE"
```

### Test Passwordless Magic Link

```bash
# Request magic link
curl -X POST http://localhost:8000/api/auth/passwordless/magic-link/request/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'

# In development, the response includes the magic link
# In production, this would be sent via email
# Click the link or use the token to authenticate
```

### Test TOTP 2FA

```bash
# Setup TOTP (requires authentication)
curl -X POST http://localhost:8000/api/auth/mfa/totp/setup/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"

# Scan the QR code with Google Authenticator or Authy
# Then verify with a code:

curl -X POST http://localhost:8000/api/auth/mfa/totp/verify/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "123456"
  }'
```

## 5. Configure OAuth/SAML (Optional)

### OAuth 2.0 Client

1. Login to admin panel
2. Go to "OAuth Clients"
3. Add a new client with:
   - Client ID
   - Client Secret
   - Redirect URIs (one per line)
   - Allowed scopes

### SAML Service Provider

1. Login to admin panel
2. Go to "SAML Service Providers"
3. Add a new SP with:
   - Entity ID
   - ACS URL
   - Certificate (optional)

## 6. Setup Request Routing

### Create Routing Rule

```bash
# Login as admin and create a routing rule:
curl -X POST http://localhost:8000/api/route/create/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example Service",
    "source_path": "/example",
    "target_url": "http://example.com/api",
    "auth_method": "jwt",
    "priority": 100
  }'
```

### Use Routing

```bash
# Forward authenticated request to target service:
curl -X GET "http://localhost:8000/api/route/forward/?target=/example" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 7. Test SOAP Endpoint

```bash
curl -X POST http://localhost:8000/api/route/soap/ \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <username>testuser</username>
    <password>testpass123</password>
  </soap:Header>
  <soap:Body>
    <target>/example</target>
    <request>Your SOAP request data</request>
  </soap:Body>
</soap:Envelope>'
```

## 8. View Authentication Logs

Authentication attempts are logged in the database.

View logs via admin panel:
1. Login to admin
2. Go to "Authentication Logs"
3. Filter by user, method, success status, etc.

## 9. API Documentation

All available endpoints are documented in the main README.md file.

Use the Django REST Framework browsable API by visiting endpoints in your browser while authenticated.

## 10. Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set secure `SECRET_KEY` from environment variable
4. Use PostgreSQL or MySQL instead of SQLite
5. Configure HTTPS
6. Set `SESSION_COOKIE_SECURE = True`
7. Set `CORS_ALLOW_ALL_ORIGINS = False`
8. Configure proper email/SMS backends for OTP
9. Setup Redis for session storage (optional)
10. Use a production WSGI server (gunicorn, uwsgi)

## Troubleshooting

### ImportError: No module named 'X'
```bash
pip install -r requirements.txt
```

### Database errors
```bash
python manage.py migrate
```

### Permission denied
Make sure you're authenticated with a valid token or session.

### CORS errors
Check CORS settings in settings.py and adjust for your frontend domain.

## Next Steps

- Explore the admin panel to understand all features
- Review the main README.md for detailed API documentation
- Configure OAuth providers for social login
- Setup LDAP/Active Directory for enterprise SSO
- Implement custom authentication backends as needed
- Add rate limiting for production use
- Setup monitoring and logging
