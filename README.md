# Authentication Services

A comprehensive Django-based authentication service that implements 16 different authentication methods with request routing capabilities supporting both REST and SOAP protocols.

## Features

### Authentication Methods Implemented

1. **Session-based authentication** - Server-side sessions with cookies
2. **Token-based authentication** - JWT tokens and API keys
3. **OAuth 2.0** - Authorization framework
4. **OpenID Connect (OIDC)** - Identity layer on OAuth 2.0
5. **SAML** - Security Assertion Markup Language
6. **Social/Federated login** - Google, GitHub, Facebook, etc.
7. **SSO with enterprise directories** - LDAP/Active Directory (configurable)
8. **SAML/OIDC + Identity Provider solutions** - Compatible with Keycloak, Okta, Auth0, Cognito
9. **Multi-factor authentication (MFA/2FA)** - TOTP with backup codes
10. **Passwordless authentication** - Magic links and one-time codes
11. **WebAuthn/FIDO2** - Passkeys, biometrics, hardware keys
12. **Mutual TLS (mTLS)** - Client certificates (configurable)
13. **API keys** - Static tokens for service authentication
14. **HMAC/signed requests** - AWS SigV4-style authentication
15. **HTTP Basic/Digest authentication** - Standard HTTP auth
16. **Kerberos/NTLM** - Windows authentication (configurable)

### Request Routing

- **REST API routing** - Forward authenticated requests to target services
- **SOAP protocol support** - Parse and route SOAP requests
- **Configurable routing rules** - Map source paths to target endpoints
- **Authentication forwarding** - Pass user context to downstream services

### Documentation

- **Interactive Documentation App** - Built-in web-based documentation
- **JSON API Documentation** - Programmatic access to docs
- **Setup Guides** - Complete installation and configuration
- **API Reference** - All endpoints with examples
- **Changelog** - Track API changes and versions

## Documentation

The service includes a comprehensive documentation app accessible at:

- **Web Interface**: http://localhost:8000/api/docs/web/
- **JSON API**: http://localhost:8000/api/docs/

### Documentation Sections

- **Setup Guide**: `/api/docs/setup/` or `/api/docs/web/setup/`
- **API Reference**: `/api/docs/api/` or `/api/docs/web/api/`
- **Changelog**: `/api/docs/changelog/` or `/api/docs/web/changelog/`
- **Architecture**: `/api/docs/architecture/`
- **Deployment**: `/api/docs/deployment/`

## Installation

### Prerequisites

- Python 3.8+
- pip
- Nox (optional, for environment management)

### Quick Setup (Manual)

1. Clone the repository:
```bash
git clone https://github.com/Vishnu-Singh/authentication-services.git
cd authentication-services
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

The service will be available at `http://localhost:8000`

### Setup with Nox (Recommended)

This project includes Nox configuration for managing different environments (dev, UAT, production).

1. Clone the repository:
```bash
git clone https://github.com/Vishnu-Singh/authentication-services.git
cd authentication-services
```

2. Install Nox:
```bash
pip install nox
```

3. Set up development environment:
```bash
# Copy environment configuration
cp .env.dev .env

# Install dependencies and run migrations
nox -s dev-install

# Create a superuser
nox -s dev-createsuperuser

# Start the development server
nox -s dev-server
```

For detailed Nox usage and environment-specific configurations, see [NOX_GUIDE.md](NOX_GUIDE.md).

## API Endpoints

### Session Authentication

- `POST /api/auth/session/register/` - Register a new user
- `POST /api/auth/session/login/` - Login with username/password
- `POST /api/auth/session/logout/` - Logout
- `GET /api/auth/session/status/` - Check session status

### JWT Token Authentication

- `POST /api/token/` - Obtain JWT token pair
- `POST /api/token/refresh/` - Refresh access token

### API Key Authentication

- `POST /api/auth/token/api-key/create/` - Create API key
- `GET /api/auth/token/api-key/list/` - List API keys
- `DELETE /api/auth/token/api-key/<id>/revoke/` - Revoke API key
- `GET /api/auth/token/api-key/verify/` - Verify API key (Header: `X-API-Key`)

### HTTP Basic Auth

- `POST /api/auth/token/basic/` - HTTP Basic authentication

### HMAC Authentication

- `POST /api/auth/token/hmac/verify/` - Verify HMAC signed request

### OAuth 2.0 / OIDC

- `GET /api/auth/oauth/authorize/` - OAuth authorization
- `POST /api/auth/oauth/token/` - Token exchange
- `GET /api/auth/oauth/userinfo/` - User information
- `GET /api/auth/oauth/.well-known/openid-configuration/` - OIDC discovery
- `POST /api/auth/oauth/social/` - Social login

### SAML

- `GET /api/auth/saml/metadata/` - SAML metadata
- `POST /api/auth/saml/sso/` - Single Sign-On
- `POST /api/auth/saml/acs/` - Assertion Consumer Service
- `POST /api/auth/saml/slo/` - Single Logout
- `GET /api/auth/saml/sp/list/` - List Service Providers

### Multi-Factor Authentication

- `POST /api/auth/mfa/totp/setup/` - Setup TOTP 2FA
- `POST /api/auth/mfa/totp/verify/` - Verify and enable TOTP
- `POST /api/auth/mfa/totp/validate/` - Validate TOTP code
- `POST /api/auth/mfa/totp/disable/` - Disable TOTP
- `POST /api/auth/mfa/webauthn/register/` - Register WebAuthn credential
- `GET /api/auth/mfa/webauthn/list/` - List WebAuthn credentials
- `DELETE /api/auth/mfa/webauthn/<id>/delete/` - Delete WebAuthn credential

### Passwordless Authentication

- `POST /api/auth/passwordless/magic-link/request/` - Request magic link
- `GET /api/auth/passwordless/magic-link/verify/` - Verify magic link
- `POST /api/auth/passwordless/otp/request/` - Request OTP
- `POST /api/auth/passwordless/otp/verify/` - Verify OTP

### Request Routing

- `GET|POST|PUT|DELETE /api/route/forward/?target=<path>` - Route authenticated request
- `POST /api/route/soap/` - SOAP endpoint
- `GET /api/route/list/` - List routing rules
- `POST /api/route/create/` - Create routing rule (admin)

## Usage Examples

### Session Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/session/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/session/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}' \
  -c cookies.txt

# Check status
curl -X GET http://localhost:8000/api/auth/session/status/ \
  -b cookies.txt
```

### JWT Token

```bash
# Get token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'

# Use token
curl -X GET http://localhost:8000/api/auth/session/status/ \
  -H "Authorization: Bearer <access_token>"
```

### API Key

```bash
# Create API key (requires authentication)
curl -X POST http://localhost:8000/api/auth/token/api-key/create/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My API Key"}'

# Use API key
curl -X GET http://localhost:8000/api/auth/token/api-key/verify/ \
  -H "X-API-Key: <api_key>"
```

### Magic Link

```bash
# Request magic link
curl -X POST http://localhost:8000/api/auth/passwordless/magic-link/request/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user1@example.com"}'

# Verify (click link or use token)
curl -X GET "http://localhost:8000/api/auth/passwordless/magic-link/verify/?token=<token>"
```

### TOTP 2FA

```bash
# Setup TOTP
curl -X POST http://localhost:8000/api/auth/mfa/totp/setup/ \
  -H "Authorization: Bearer <access_token>"

# Verify TOTP code
curl -X POST http://localhost:8000/api/auth/mfa/totp/verify/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'
```

### Request Routing

```bash
# Create routing rule (admin)
curl -X POST http://localhost:8000/api/route/create/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "User Service",
    "source_path": "/users",
    "target_url": "http://backend.example.com/api/users",
    "auth_method": "jwt"
  }'

# Forward request
curl -X GET "http://localhost:8000/api/route/forward/?target=/users" \
  -H "Authorization: Bearer <access_token>"
```

### SOAP Request

```xml
POST /api/route/soap/ HTTP/1.1
Content-Type: text/xml

<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <username>user1</username>
    <password>password123</password>
  </soap:Header>
  <soap:Body>
    <target>/service-name</target>
    <request>
      <!-- Your SOAP request here -->
    </request>
  </soap:Body>
</soap:Envelope>
```

## Configuration

Edit `auth_service/settings.py` to configure:

- Database settings
- OAuth providers (Google, GitHub, etc.)
- SAML configuration
- LDAP/Active Directory settings
- JWT token expiration
- WebAuthn settings
- Email/SMS providers for OTP

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage:

- Users and permissions
- API keys
- OAuth clients
- SAML service providers
- Routing rules
- Authentication logs

## Security Considerations

- In production, set `DEBUG = False`
- Use HTTPS for all endpoints
- Set strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Enable CORS properly with `CORS_ALLOW_ALL_ORIGINS = False`
- Use environment variables for sensitive configuration
- Implement rate limiting
- Enable CSRF protection for session-based auth
- Use secure session cookies with `SESSION_COOKIE_SECURE = True`

## Testing

Run tests with:
```bash
python manage.py test
```

## Architecture

The service is organized into multiple Django apps:

- **auth_core** - Core models (API keys, OAuth clients, routing rules, logs)
- **auth_session** - Session-based authentication
- **auth_token** - Token-based authentication (JWT, API keys, HMAC, Basic)
- **auth_oauth** - OAuth 2.0 and OIDC
- **auth_saml** - SAML authentication
- **auth_mfa** - Multi-factor authentication
- **auth_passwordless** - Passwordless authentication
- **auth_api_routing** - Request routing for REST and SOAP

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues and questions, please open a GitHub issue.