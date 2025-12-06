# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Authentication Service (Django)                   │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     API Gateway Layer                       │    │
│  │  - REST API (Django REST Framework)                         │    │
│  │  - SOAP Protocol Support                                    │    │
│  │  - Request Routing & Forwarding                             │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                        │
│  ┌───────────────────────────┼────────────────────────────────┐    │
│  │        Authentication Modules                               │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │   Session    │  │     JWT      │  │   API Keys   │    │    │
│  │  │     Auth     │  │    Tokens    │  │    (HMAC)    │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │   OAuth 2.0  │  │     OIDC     │  │  Social Auth │    │    │
│  │  │   + Social   │  │  (Discovery) │  │ (G/FB/GH/etc)│    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │     SAML     │  │   LDAP/AD    │  │   Kerberos   │    │    │
│  │  │   (IdP/SP)   │  │     SSO      │  │     NTLM     │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │  MFA / 2FA   │  │ Passwordless │  │  WebAuthn/   │    │    │
│  │  │    (TOTP)    │  │ Magic Link/  │  │    FIDO2     │    │    │
│  │  │ Backup Codes │  │     OTP      │  │   Passkeys   │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │ HTTP Basic/  │  │     mTLS     │  │   Custom     │    │    │
│  │  │    Digest    │  │ Client Certs │  │   Methods    │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                        │
│  ┌───────────────────────────┼────────────────────────────────┐    │
│  │              Core Services & Middleware                     │    │
│  │                                                              │    │
│  │  • Authentication Logging                                   │    │
│  │  • User Session Management                                  │    │
│  │  • Token Validation & Refresh                               │    │
│  │  • CORS Handling                                            │    │
│  │  • Security Middleware                                      │    │
│  │  • Rate Limiting (configurable)                             │    │
│  └──────────────────────────────────────────────────────────┘    │
│                              │                                        │
│  ┌───────────────────────────┼────────────────────────────────┐    │
│  │                     Data Layer                              │    │
│  │                                                              │    │
│  │  ┌────────────────────────────────────────────────────┐   │    │
│  │  │              Database Models                        │   │    │
│  │  │  • User (Django built-in)                           │   │    │
│  │  │  • APIKey                                            │   │    │
│  │  │  • OAuthClient                                       │   │    │
│  │  │  • SAMLServiceProvider                               │   │    │
│  │  │  • RoutingRule                                       │   │    │
│  │  │  • AuthenticationLog                                 │   │    │
│  │  │  • TOTPDevice                                        │   │    │
│  │  │  • BackupCode                                        │   │    │
│  │  │  • WebAuthnCredential                                │   │    │
│  │  │  • MagicLink                                         │   │    │
│  │  │  • OneTimeCode                                       │   │    │
│  │  └────────────────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │
      ┌───────────────────────┼───────────────────────┐
      │                       │                       │
      ▼                       ▼                       ▼
┌──────────┐          ┌──────────┐           ┌──────────┐
│ External │          │ Backend  │           │ Frontend │
│ Identity │          │ Services │           │  Apps    │
│ Provider │          │ (Target) │           │          │
│ (IdP)    │          └──────────┘           └──────────┘
└──────────┘
  - Okta
  - Auth0
  - Keycloak
  - Cognito
  - LDAP/AD
```

## Request Flow

### 1. Authentication Flow

```
Client Request
    │
    ├─► Session Auth ──► Django Session ──► Response
    │
    ├─► JWT Token ──► Verify Token ──► Response
    │
    ├─► API Key ──► Validate Key ──► Response
    │
    ├─► OAuth/OIDC ──► External IdP ──► Token Exchange ──► Response
    │
    ├─► SAML ──► Parse Assertion ──► Validate ──► Response
    │
    ├─► MFA ──► Base Auth ──► TOTP/WebAuthn ──► Response
    │
    └─► Passwordless ──► Magic Link/OTP ──► Verify ──► Response
```

### 2. Request Routing Flow

```
Incoming Request
    │
    ▼
┌────────────────┐
│ Authentication │
│   Validation   │
└────────────────┘
    │
    ▼
┌────────────────┐
│  Find Routing  │
│      Rule      │
└────────────────┘
    │
    ▼
┌────────────────┐
│ Forward Request│
│  to Target     │
│    Service     │
└────────────────┘
    │
    ▼
┌────────────────┐
│ Target Service │
│   Processes    │
│    Request     │
└────────────────┘
    │
    ▼
┌────────────────┐
│ Return Response│
│  to Client     │
└────────────────┘
```

## Component Responsibilities

### Auth Core App
- Central models (APIKey, OAuthClient, SAMLServiceProvider, RoutingRule)
- Authentication logging
- Admin interfaces

### Auth Session App
- Traditional session-based authentication
- User registration
- Login/Logout endpoints

### Auth Token App
- JWT token generation and validation
- API key management
- HMAC signature verification
- HTTP Basic authentication

### Auth OAuth App
- OAuth 2.0 authorization server
- OpenID Connect provider
- Social authentication integration

### Auth SAML App
- SAML Identity Provider
- SAML Service Provider
- Metadata generation
- SSO and SLO

### Auth MFA App
- TOTP (Google Authenticator, Authy)
- Backup codes
- WebAuthn/FIDO2 credentials
- Passkeys support

### Auth Passwordless App
- Magic link generation
- One-time password (OTP)
- Email/SMS delivery

### Auth API Routing App
- Request forwarding
- Protocol translation (REST/SOAP)
- Route management
- User context forwarding

## Security Features

1. **Token Management**
   - JWT with configurable expiration
   - Refresh token rotation
   - Token blacklisting

2. **Session Security**
   - Secure cookies
   - CSRF protection
   - HTTP-only flags
   - SameSite policy

3. **API Security**
   - CORS configuration
   - Rate limiting (configurable)
   - API key expiration
   - HMAC signature verification

4. **Authentication Logging**
   - All authentication attempts logged
   - IP address tracking
   - User agent recording
   - Success/failure tracking

5. **Multi-Factor Authentication**
   - Time-based OTP
   - Backup codes
   - Hardware security keys
   - Biometric authentication

## Scalability Considerations

1. **Database**
   - Supports PostgreSQL, MySQL, SQLite
   - Indexed fields for performance
   - Connection pooling

2. **Caching**
   - Redis support for sessions
   - Token caching
   - API key caching

3. **Load Balancing**
   - Stateless JWT authentication
   - Session store in Redis/database
   - Horizontal scaling support

4. **Monitoring**
   - Authentication logs
   - Failed login tracking
   - Performance metrics

## Integration Points

1. **Identity Providers**
   - SAML metadata exchange
   - OAuth client registration
   - LDAP/AD connection

2. **Backend Services**
   - REST API forwarding
   - SOAP protocol support
   - Header-based user context

3. **Frontend Applications**
   - CORS-enabled endpoints
   - Token-based authentication
   - Session cookie support

4. **External Services**
   - Email providers (SendGrid, AWS SES)
   - SMS providers (Twilio)
   - Social platforms (Google, GitHub, Facebook)
