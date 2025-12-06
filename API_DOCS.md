# API Documentation

## Base URL
`http://localhost:8000`

## Authentication Methods

All endpoints support one or more of the following authentication methods:

1. **Session Cookie** - Use session-based authentication
2. **JWT Bearer Token** - Include `Authorization: Bearer <token>` header
3. **API Key** - Include `X-API-Key: <key>` header
4. **HTTP Basic Auth** - Include `Authorization: Basic <base64(username:password)>` header

---

## Session Authentication

### Register User
```
POST /api/auth/session/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

### Login
```
POST /api/auth/session/login/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  },
  "session_id": "string"
}
```

### Logout
```
POST /api/auth/session/logout/
Authorization: Session Cookie
```

**Response (200):**
```json
{
  "message": "Logout successful"
}
```

### Check Session Status
```
GET /api/auth/session/status/
Authorization: Session Cookie
```

**Response (200):**
```json
{
  "authenticated": true,
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

---

## JWT Token Authentication

### Obtain Token
```
POST /api/token/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

### Refresh Token
```
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

---

## API Key Management

### Create API Key
```
POST /api/auth/token/api-key/create/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "string",
  "expires_at": "2025-12-31T23:59:59Z" (optional)
}
```

**Response (201):**
```json
{
  "message": "API key created successfully",
  "api_key": {
    "id": 1,
    "name": "string",
    "key": "generated-key-here",
    "created_at": "2025-12-06T20:00:00Z",
    "expires_at": null
  }
}
```

### List API Keys
```
GET /api/auth/token/api-key/list/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "api_keys": [
    {
      "id": 1,
      "name": "string",
      "key": "12345678...",
      "is_active": true,
      "created_at": "2025-12-06T20:00:00Z",
      "last_used": null,
      "expires_at": null
    }
  ]
}
```

### Verify API Key
```
GET /api/auth/token/api-key/verify/
X-API-Key: <api-key>
```

**Response (200):**
```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "string",
    "email": "string"
  }
}
```

### Revoke API Key
```
DELETE /api/auth/token/api-key/<key_id>/revoke/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "message": "API key revoked successfully"
}
```

---

## OAuth 2.0 / OIDC

### Authorization Endpoint
```
GET /api/auth/oauth/authorize/
  ?client_id=<client_id>
  &redirect_uri=<redirect_uri>
  &response_type=code
  &scope=openid profile email
  &state=<state>
```

### Token Exchange
```
POST /api/auth/oauth/token/
Content-Type: application/json

{
  "grant_type": "authorization_code",
  "code": "string",
  "client_id": "string",
  "client_secret": "string",
  "redirect_uri": "string"
}
```

### UserInfo
```
GET /api/auth/oauth/userinfo/
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "sub": "1",
  "name": "John Doe",
  "preferred_username": "johndoe",
  "email": "john@example.com",
  "email_verified": true
}
```

### OIDC Discovery
```
GET /api/auth/oauth/.well-known/openid-configuration/
```

### Social Login
```
POST /api/auth/oauth/social/
Content-Type: application/json

{
  "provider": "google|github|facebook",
  "access_token": "string"
}
```

---

## SAML

### Metadata
```
GET /api/auth/saml/metadata/
```

### Single Sign-On
```
POST /api/auth/saml/sso/
Content-Type: application/x-www-form-urlencoded

SAMLRequest=<base64_encoded_request>
&RelayState=<state>
```

### Assertion Consumer Service
```
POST /api/auth/saml/acs/
Content-Type: application/x-www-form-urlencoded

SAMLResponse=<base64_encoded_response>
&RelayState=<state>
```

---

## Multi-Factor Authentication

### Setup TOTP
```
POST /api/auth/mfa/totp/setup/
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "secret": "BASE32SECRET",
  "qr_code": "data:image/png;base64,...",
  "provisioning_uri": "otpauth://totp/...",
  "message": "Scan the QR code with your authenticator app"
}
```

### Verify TOTP
```
POST /api/auth/mfa/totp/verify/
Authorization: Bearer <token>
Content-Type: application/json

{
  "code": "123456"
}
```

**Response (200):**
```json
{
  "message": "TOTP enabled successfully",
  "backup_codes": ["CODE1", "CODE2", ...],
  "note": "Save these backup codes in a safe place"
}
```

### Validate TOTP
```
POST /api/auth/mfa/totp/validate/
Content-Type: application/json

{
  "username": "string",
  "code": "123456"
}
```

### WebAuthn Registration
```
POST /api/auth/mfa/webauthn/register/
Authorization: Bearer <token>
Content-Type: application/json

{
  "credential_id": "string",
  "public_key": "string",
  "name": "My Security Key"
}
```

---

## Passwordless Authentication

### Request Magic Link
```
POST /api/auth/passwordless/magic-link/request/
Content-Type: application/json

{
  "email": "string"
}
```

**Response (200):**
```json
{
  "message": "Magic link sent to your email",
  "expires_in": "15 minutes"
}
```

### Verify Magic Link
```
GET /api/auth/passwordless/magic-link/verify/?token=<token>
```

### Request OTP
```
POST /api/auth/passwordless/otp/request/
Content-Type: application/json

{
  "email": "string",
  "method": "email|sms"
}
```

### Verify OTP
```
POST /api/auth/passwordless/otp/verify/
Content-Type: application/json

{
  "email": "string",
  "code": "123456"
}
```

---

## Request Routing

### Forward Request
```
GET|POST|PUT|DELETE /api/route/forward/?target=<path>
Authorization: Bearer <token>
```

### List Routes
```
GET /api/route/list/
Authorization: Bearer <token>
```

### Create Route (Admin)
```
POST /api/route/create/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "string",
  "source_path": "string",
  "target_url": "string",
  "auth_method": "session|jwt|oauth|saml|api_key",
  "priority": 100
}
```

### SOAP Endpoint
```
POST /api/route/soap/
Content-Type: text/xml

<?xml version="1.0"?>
<soap:Envelope>
  <soap:Header>
    <username>user</username>
    <password>pass</password>
  </soap:Header>
  <soap:Body>
    <target>/service</target>
  </soap:Body>
</soap:Envelope>
```

---

## HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - Routing error

## Error Response Format

```json
{
  "error": "Error message description"
}
```
