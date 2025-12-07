from datetime import datetime

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def docs_home(request):
    """
    Documentation home page - serves as the landing page for all documentation.
    """
    return Response(
        {
            "message": "Authentication Service Documentation",
            "version": "1.0.0",
            "documentation_sections": {
                "setup": "/api/docs/setup/",
                "api_reference": "/api/docs/api/",
                "changelog": "/api/docs/changelog/",
                "architecture": "/api/docs/architecture/",
                "deployment": "/api/docs/deployment/",
            },
            "note": "Visit individual endpoints for detailed documentation",
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def setup_guide(request):
    """
    Project setup and installation guide.
    """
    setup_info = {
        "title": "Authentication Service - Setup Guide",
        "version": "1.0.0",
        "last_updated": "2025-12-07",
        "prerequisites": {
            "python": "3.8+",
            "pip": "Latest version",
            "database": "SQLite (dev) / PostgreSQL or MySQL (production)",
            "optional": [
                "Redis (for session storage)",
                "Docker (for containerization)",
            ],
        },
        "installation_steps": [
            {
                "step": 1,
                "title": "Clone Repository",
                "command": "git clone https://github.com/Vishnu-Singh/authentication-services.git\ncd authentication-services",
            },
            {
                "step": 2,
                "title": "Install Dependencies",
                "command": "pip install -r requirements.txt",
            },
            {
                "step": 3,
                "title": "Run Database Migrations",
                "command": "python manage.py migrate",
            },
            {
                "step": 4,
                "title": "Create Superuser",
                "command": "python manage.py createsuperuser",
            },
            {
                "step": 5,
                "title": "Start Development Server",
                "command": "python manage.py runserver",
            },
        ],
        "configuration": {
            "environment_file": ".env",
            "example_provided": ".env.example",
            "key_settings": [
                "DEBUG - Set to False in production",
                "SECRET_KEY - Use a strong random key",
                "ALLOWED_HOSTS - Configure allowed domains",
                "DATABASE_* - Database connection settings",
                "CORS_ALLOWED_ORIGINS - Configure CORS for frontend",
                "EMAIL_* - Email configuration for OTP/magic links",
            ],
        },
        "project_structure": {
            "auth_service": "Main Django project configuration",
            "auth_core": "Core models (APIKey, OAuthClient, RoutingRule, etc.)",
            "auth_session": "Session-based authentication",
            "auth_token": "Token/API key authentication",
            "auth_oauth": "OAuth 2.0 and OIDC",
            "auth_saml": "SAML authentication",
            "auth_mfa": "Multi-factor authentication",
            "auth_passwordless": "Passwordless authentication",
            "auth_api_routing": "Request routing (REST/SOAP)",
            "docs": "Documentation app",
        },
        "quick_test": {
            "description": "Quick test to verify installation",
            "steps": [
                "Start server: python manage.py runserver",
                "Visit admin: http://localhost:8000/admin/",
                "Check API: http://localhost:8000/api/docs/",
                "Test endpoint: curl http://localhost:8000/api/auth/session/status/",
            ],
        },
        "troubleshooting": [
            {
                "issue": "Module not found errors",
                "solution": "Run: pip install -r requirements.txt",
            },
            {"issue": "Database errors", "solution": "Run: python manage.py migrate"},
            {
                "issue": "Port already in use",
                "solution": "Use different port: python manage.py runserver 8001",
            },
        ],
    }

    return Response(setup_info)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    Comprehensive API documentation with all endpoints.
    """
    api_docs = {
        "title": "Authentication Service - API Reference",
        "version": "1.0.0",
        "base_url": "http://localhost:8000",
        "authentication": {
            "methods": [
                "Session Cookie",
                "JWT ****** (Authorization: ******)",
                "API Key (X-API-Key: <key>)",
                "HTTP Basic Auth",
            ]
        },
        "endpoints": {
            "session_auth": {
                "base_path": "/api/auth/session/",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/auth/session/register/",
                        "description": "Register new user",
                        "auth_required": False,
                        "request_body": {
                            "username": "string (required)",
                            "email": "string (required)",
                            "password": "string (required)",
                        },
                        "response": {
                            "status": 201,
                            "body": {
                                "message": "User registered successfully",
                                "user": {
                                    "id": "int",
                                    "username": "string",
                                    "email": "string",
                                },
                            },
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/auth/session/login/",
                        "description": "Login with credentials",
                        "auth_required": False,
                        "request_body": {
                            "username": "string (required)",
                            "password": "string (required)",
                        },
                        "response": {
                            "status": 200,
                            "body": {
                                "message": "Login successful",
                                "user": {
                                    "id": "int",
                                    "username": "string",
                                    "email": "string",
                                },
                                "session_id": "string",
                            },
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/auth/session/logout/",
                        "description": "Logout and destroy session",
                        "auth_required": True,
                        "response": {
                            "status": 200,
                            "body": {"message": "Logout successful"},
                        },
                    },
                    {
                        "method": "GET",
                        "path": "/api/auth/session/status/",
                        "description": "Check authentication status",
                        "auth_required": True,
                        "response": {
                            "status": 200,
                            "body": {
                                "authenticated": True,
                                "user": {
                                    "id": "int",
                                    "username": "string",
                                    "email": "string",
                                },
                            },
                        },
                    },
                ],
            },
            "jwt_auth": {
                "base_path": "/api/token/",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/token/",
                        "description": "Obtain JWT access and refresh tokens",
                        "auth_required": False,
                        "request_body": {
                            "username": "string (required)",
                            "password": "string (required)",
                        },
                        "response": {
                            "status": 200,
                            "body": {
                                "access": "string (JWT)",
                                "refresh": "string (JWT)",
                            },
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/token/refresh/",
                        "description": "Refresh JWT access token",
                        "auth_required": False,
                        "request_body": {"refresh": "string (required)"},
                        "response": {"status": 200, "body": {"access": "string (JWT)"}},
                    },
                ],
            },
            "api_keys": {
                "base_path": "/api/auth/token/api-key/",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/auth/token/api-key/create/",
                        "description": "Create new API key",
                        "auth_required": True,
                        "request_body": {
                            "name": "string (required)",
                            "expires_at": "datetime (optional)",
                        },
                        "response": {
                            "status": 201,
                            "body": {
                                "message": "API key created successfully",
                                "api_key": {
                                    "id": "int",
                                    "name": "string",
                                    "key": "string",
                                    "created_at": "datetime",
                                    "expires_at": "datetime or null",
                                },
                            },
                        },
                    },
                    {
                        "method": "GET",
                        "path": "/api/auth/token/api-key/list/",
                        "description": "List all API keys for authenticated user",
                        "auth_required": True,
                        "response": {
                            "status": 200,
                            "body": {
                                "api_keys": [
                                    {
                                        "id": "int",
                                        "name": "string",
                                        "key": "string",
                                        "is_active": "bool",
                                    }
                                ]
                            },
                        },
                    },
                    {
                        "method": "GET",
                        "path": "/api/auth/token/api-key/verify/",
                        "description": "Verify API key validity",
                        "auth_required": False,
                        "headers": {"X-API-Key": "string (required)"},
                        "response": {
                            "status": 200,
                            "body": {
                                "valid": True,
                                "user": {
                                    "id": "int",
                                    "username": "string",
                                    "email": "string",
                                },
                            },
                        },
                    },
                    {
                        "method": "DELETE",
                        "path": "/api/auth/token/api-key/<id>/revoke/",
                        "description": "Revoke/delete API key",
                        "auth_required": True,
                        "response": {
                            "status": 200,
                            "body": {"message": "API key revoked successfully"},
                        },
                    },
                ],
            },
            "oauth": {
                "base_path": "/api/auth/oauth/",
                "endpoints": [
                    {
                        "method": "GET",
                        "path": "/api/auth/oauth/authorize/",
                        "description": "OAuth 2.0 authorization endpoint",
                        "auth_required": False,
                        "query_params": {
                            "client_id": "string (required)",
                            "redirect_uri": "string (required)",
                            "response_type": "string (default: code)",
                            "scope": "string (default: openid profile email)",
                            "state": "string (optional)",
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/auth/oauth/token/",
                        "description": "Exchange authorization code for access token",
                        "auth_required": False,
                        "request_body": {
                            "grant_type": "authorization_code",
                            "code": "string (required)",
                            "client_id": "string (required)",
                            "client_secret": "string (required)",
                            "redirect_uri": "string (required)",
                        },
                    },
                    {
                        "method": "GET",
                        "path": "/api/auth/oauth/.well-known/openid-configuration/",
                        "description": "OpenID Connect discovery endpoint",
                        "auth_required": False,
                    },
                ],
            },
            "mfa": {
                "base_path": "/api/auth/mfa/",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/auth/mfa/totp/setup/",
                        "description": "Setup TOTP 2FA with QR code",
                        "auth_required": True,
                        "response": {
                            "status": 200,
                            "body": {
                                "secret": "string",
                                "qr_code": "string (base64 image)",
                                "provisioning_uri": "string",
                            },
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/auth/mfa/totp/verify/",
                        "description": "Verify TOTP code and enable 2FA",
                        "auth_required": True,
                        "request_body": {"code": "string (6 digits)"},
                        "response": {
                            "status": 200,
                            "body": {
                                "message": "TOTP enabled successfully",
                                "backup_codes": ["string", "string", "..."],
                            },
                        },
                    },
                ],
            },
            "passwordless": {
                "base_path": "/api/auth/passwordless/",
                "endpoints": [
                    {
                        "method": "POST",
                        "path": "/api/auth/passwordless/magic-link/request/",
                        "description": "Request magic link for passwordless login",
                        "auth_required": False,
                        "request_body": {"email": "string (required)"},
                        "response": {
                            "status": 200,
                            "body": {"message": "Magic link sent to your email"},
                        },
                    },
                    {
                        "method": "POST",
                        "path": "/api/auth/passwordless/otp/request/",
                        "description": "Request one-time password",
                        "auth_required": False,
                        "request_body": {
                            "email": "string (required)",
                            "method": "email or sms",
                        },
                    },
                ],
            },
            "routing": {
                "base_path": "/api/route/",
                "endpoints": [
                    {
                        "method": "GET|POST|PUT|DELETE|PATCH",
                        "path": "/api/route/forward/",
                        "description": "Forward authenticated request to target service",
                        "auth_required": True,
                        "query_params": {"target": "string (required - routing path)"},
                        "note": "Returns response from target service",
                    },
                    {
                        "method": "POST",
                        "path": "/api/route/soap/",
                        "description": "SOAP endpoint for routing",
                        "auth_required": False,
                        "content_type": "text/xml",
                        "note": "Parses SOAP envelope and forwards to target",
                    },
                    {
                        "method": "GET",
                        "path": "/api/route/list/",
                        "description": "List all routing rules",
                        "auth_required": True,
                    },
                    {
                        "method": "POST",
                        "path": "/api/route/create/",
                        "description": "Create new routing rule (admin only)",
                        "auth_required": True,
                        "request_body": {
                            "name": "string (required)",
                            "source_path": "string (required)",
                            "target_url": "string (required)",
                            "auth_method": "string (session|jwt|oauth|saml|api_key)",
                            "priority": "int (default: 100)",
                        },
                    },
                ],
            },
        },
        "error_responses": {
            "400": "Bad Request - Invalid input",
            "401": "Unauthorized - Authentication required",
            "403": "Forbidden - Permission denied",
            "404": "Not Found - Resource not found",
            "500": "Internal Server Error",
            "502": "Bad Gateway - Routing error",
        },
        "rate_limiting": {
            "note": "Configure rate limiting in production",
            "recommended": "100 requests per minute per user",
        },
    }

    return Response(api_docs)


@api_view(["GET"])
@permission_classes([AllowAny])
def changelog(request):
    """
    API changelog and version history.
    """
    changelog_data = {
        "title": "Authentication Service - Changelog",
        "current_version": "1.0.0",
        "versions": [
            {
                "version": "1.0.0",
                "release_date": "2025-12-07",
                "status": "Current",
                "changes": {
                    "added": [
                        "Session-based authentication with cookies",
                        "JWT token authentication with refresh",
                        "OAuth 2.0 authorization server",
                        "OpenID Connect (OIDC) provider",
                        "SAML Identity Provider",
                        "Social login framework",
                        "LDAP/Active Directory support",
                        "Multi-factor authentication (TOTP)",
                        "Backup codes for MFA",
                        "WebAuthn/FIDO2 credentials",
                        "Passwordless magic links",
                        "One-time password (OTP)",
                        "API key management",
                        "HMAC signed requests",
                        "HTTP Basic authentication",
                        "Request routing for REST",
                        "SOAP protocol support",
                        "Authentication audit logging",
                        "Django admin interfaces",
                        "Documentation app",
                        "Comprehensive API documentation",
                        "Setup and deployment guides",
                    ],
                    "security": [
                        "CORS configuration",
                        "CSRF protection",
                        "Secure session cookies",
                        "JWT token blacklisting support",
                        "API key expiration",
                        "IP address tracking",
                        "User agent logging",
                    ],
                    "infrastructure": [
                        "PostgreSQL/MySQL support",
                        "Redis session storage support",
                        "Docker deployment configuration",
                        "Production deployment guide",
                    ],
                },
                "breaking_changes": [],
                "deprecated": [],
                "bug_fixes": [],
            }
        ],
        "upcoming": {
            "version": "1.1.0",
            "planned_features": [
                "Rate limiting middleware",
                "Email/SMS provider integration",
                "Full LDAP/AD implementation",
                "Advanced SAML features",
                "GraphQL API support",
                "Webhook notifications",
                "Analytics dashboard",
                "API documentation UI (Swagger/ReDoc)",
            ],
        },
        "migration_guide": {
            "from_0_to_1": {
                "steps": [
                    "This is the initial release",
                    "Follow setup guide for installation",
                    "Run migrations: python manage.py migrate",
                    "Create superuser for admin access",
                ]
            }
        },
        "api_versioning": {
            "strategy": "URL path versioning (future)",
            "current": "Single version (v1 implicit)",
            "note": "Future versions will use /api/v2/ prefix",
        },
    }

    return Response(changelog_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def architecture_docs(request):
    """
    System architecture documentation.
    """
    architecture = {
        "title": "Authentication Service - Architecture",
        "version": "1.0.0",
        "overview": {
            "type": "Microservice Authentication Gateway",
            "framework": "Django 6.0",
            "architecture_pattern": "Modular Monolith",
            "deployment": "Containerized (Docker) or Traditional (WSGI)",
        },
        "components": {
            "django_apps": {
                "auth_core": {
                    "purpose": "Core models and shared utilities",
                    "models": [
                        "APIKey",
                        "OAuthClient",
                        "SAMLServiceProvider",
                        "RoutingRule",
                        "AuthenticationLog",
                    ],
                    "responsibilities": [
                        "Shared data models",
                        "Admin interfaces",
                        "Common utilities",
                    ],
                },
                "auth_session": {
                    "purpose": "Session-based authentication",
                    "features": [
                        "User registration",
                        "Login/Logout",
                        "Session management",
                    ],
                },
                "auth_token": {
                    "purpose": "Token-based authentication",
                    "features": [
                        "JWT tokens",
                        "API keys",
                        "HMAC signing",
                        "HTTP Basic auth",
                    ],
                },
                "auth_oauth": {
                    "purpose": "OAuth 2.0 and OIDC",
                    "features": [
                        "Authorization server",
                        "Token exchange",
                        "Social login",
                    ],
                },
                "auth_saml": {
                    "purpose": "SAML authentication",
                    "features": [
                        "Identity Provider",
                        "Service Provider",
                        "Metadata generation",
                    ],
                },
                "auth_mfa": {
                    "purpose": "Multi-factor authentication",
                    "features": ["TOTP", "Backup codes", "WebAuthn/FIDO2"],
                },
                "auth_passwordless": {
                    "purpose": "Passwordless authentication",
                    "features": ["Magic links", "One-time codes"],
                },
                "auth_api_routing": {
                    "purpose": "Request routing and protocol translation",
                    "features": [
                        "REST forwarding",
                        "SOAP support",
                        "User context forwarding",
                    ],
                },
                "docs": {
                    "purpose": "API documentation",
                    "features": ["Setup guide", "API reference", "Changelog"],
                },
            },
            "database": {
                "development": "SQLite",
                "production": "PostgreSQL or MySQL recommended",
                "models_count": 11,
                "features": ["Migrations", "Indexing", "Foreign keys"],
            },
            "caching": {
                "optional": True,
                "backend": "Redis",
                "use_cases": ["Session storage", "Token caching", "Rate limiting"],
            },
        },
        "request_flow": {
            "authentication": [
                "1. Client sends request with credentials",
                "2. Authentication middleware validates credentials",
                "3. User object attached to request",
                "4. View processes authenticated request",
                "5. Response returned to client",
            ],
            "routing": [
                "1. Authenticated request received",
                "2. Routing rule matched by path",
                "3. User context added to headers",
                "4. Request forwarded to target service",
                "5. Target service response returned",
            ],
        },
        "security_layers": [
            "HTTPS/TLS encryption",
            "CORS configuration",
            "CSRF protection",
            "Session security",
            "Token validation",
            "API key verification",
            "Audit logging",
        ],
        "scalability": {
            "horizontal": "Stateless JWT enables multiple instances",
            "session_storage": "Redis for distributed sessions",
            "database": "Connection pooling and read replicas",
            "load_balancing": "Nginx or cloud load balancer",
        },
        "integration_points": {
            "identity_providers": ["SAML", "OAuth", "LDAP", "Active Directory"],
            "backend_services": ["REST APIs", "SOAP services"],
            "frontend_apps": ["Web applications", "Mobile apps", "SPAs"],
            "external_services": [
                "Email providers",
                "SMS gateways",
                "Social platforms",
            ],
        },
    }

    return Response(architecture)


@api_view(["GET"])
@permission_classes([AllowAny])
def deployment_guide(request):
    """
    Deployment guide and best practices.
    """
    deployment = {
        "title": "Authentication Service - Deployment Guide",
        "version": "1.0.0",
        "environments": {
            "development": {
                "database": "SQLite",
                "debug": True,
                "server": "Django development server",
                "setup": "python manage.py runserver",
            },
            "staging": {
                "database": "PostgreSQL",
                "debug": False,
                "server": "Gunicorn + Nginx",
                "features": ["SSL certificate", "Environment variables"],
            },
            "production": {
                "database": "PostgreSQL with replicas",
                "debug": False,
                "server": "Gunicorn + Nginx + Load Balancer",
                "features": ["SSL/TLS", "Redis caching", "Monitoring", "Backups"],
            },
        },
        "deployment_options": {
            "traditional": {
                "components": ["Gunicorn", "Nginx", "PostgreSQL", "Redis"],
                "steps": [
                    "1. Setup server (Ubuntu/CentOS)",
                    "2. Install dependencies",
                    "3. Configure database",
                    "4. Setup Gunicorn service",
                    "5. Configure Nginx",
                    "6. Obtain SSL certificate",
                    "7. Configure firewall",
                ],
            },
            "docker": {
                "components": ["Docker", "Docker Compose"],
                "services": ["web", "db", "redis", "nginx"],
                "command": "docker-compose up -d",
            },
            "cloud": {
                "aws": ["EC2", "RDS", "ElastiCache", "ALB"],
                "azure": ["App Service", "Azure Database", "Redis Cache"],
                "gcp": ["App Engine", "Cloud SQL", "Memorystore"],
            },
        },
        "configuration_checklist": [
            "Set DEBUG=False",
            "Configure strong SECRET_KEY",
            "Set ALLOWED_HOSTS",
            "Configure database (PostgreSQL/MySQL)",
            "Setup email backend",
            "Configure CORS_ALLOWED_ORIGINS",
            "Enable secure cookies (HTTPS)",
            "Setup Redis for sessions",
            "Configure logging",
            "Setup monitoring",
        ],
        "security_checklist": [
            "Use HTTPS/SSL everywhere",
            "Strong SECRET_KEY from environment",
            "Secure database credentials",
            "Enable firewall (UFW/firewalld)",
            "Configure fail2ban",
            "Regular security updates",
            "Enable audit logging",
            "Setup backup strategy",
            "Monitor failed login attempts",
            "Use environment variables for secrets",
        ],
        "performance_optimization": [
            "Enable database connection pooling",
            "Use Redis for session storage",
            "Enable database query optimization",
            "Setup CDN for static files",
            "Enable Gzip compression",
            "Configure caching headers",
            "Use database indexes",
            "Monitor slow queries",
        ],
        "monitoring": {
            "logs": [
                "Application logs",
                "Access logs",
                "Error logs",
                "Authentication logs",
            ],
            "metrics": [
                "Request rate",
                "Response time",
                "Error rate",
                "Database queries",
            ],
            "tools": ["Prometheus", "Grafana", "ELK Stack", "Sentry"],
        },
        "backup_strategy": {
            "database": "Daily automated backups with retention",
            "files": "Backup uploaded files and configurations",
            "testing": "Regular restore testing",
        },
    }

    return Response(deployment)


def docs_web_home(request):
    """
    Web-based documentation home page with navigation.
    """
    return render(
        request,
        "docs/home.html",
        {"title": "Authentication Service Documentation", "version": "1.0.0"},
    )


def docs_web_setup(request):
    """
    Web-based setup guide.
    """
    return render(request, "docs/setup.html", {"title": "Setup Guide"})


def docs_web_api(request):
    """
    Web-based API documentation.
    """
    return render(request, "docs/api.html", {"title": "API Reference"})


def docs_web_changelog(request):
    """
    Web-based changelog.
    """
    return render(request, "docs/changelog.html", {"title": "Changelog"})
