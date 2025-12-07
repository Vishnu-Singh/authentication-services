"""
UAT (User Acceptance Testing) environment settings for auth_service project.

This module extends the base settings with UAT-specific configurations.
"""

import os
from pathlib import Path

from decouple import Csv, config

from .settings import *

# UAT mode - limited debug
DEBUG = config("DEBUG", default=False, cast=bool)

# Environment indicator
ENVIRONMENT = "uat"

# Restricted hosts in UAT
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Database - Use PostgreSQL or environment-configured database
DATABASES = {
    "default": {
        "ENGINE": config("DATABASE_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DATABASE_NAME", default=str(BASE_DIR / "db_uat.sqlite3")),
        "USER": config("DATABASE_USER", default=""),
        "PASSWORD": config("DATABASE_PASSWORD", default=""),
        "HOST": config("DATABASE_HOST", default=""),
        "PORT": config("DATABASE_PORT", default=""),
    }
}

# CORS - Restricted origins
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", default="http://localhost:3000", cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# Session Configuration - Secure for UAT
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=True, cast=bool)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# CSRF Configuration - Secure for UAT
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=True, cast=bool)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS", default="https://uat.example.com", cast=Csv()
)

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles_uat"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media_uat"

# Email backend - Use SMTP for UAT
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@uat.example.com")

# Logging configuration for UAT
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "uat.log",
            "maxBytes": 1024 * 1024 * 15,  # 15MB
            "backupCount": 10,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "auth_service": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Create logs directory if it doesn't exist
import os

logs_dir = BASE_DIR / "logs"
os.makedirs(logs_dir, exist_ok=True)

# UAT-specific JWT settings
from datetime import timedelta

SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    }
)

# WebAuthn settings for UAT
WEBAUTHN_RP_ID = config("WEBAUTHN_RP_ID", default="uat.example.com")
WEBAUTHN_RP_NAME = config("WEBAUTHN_RP_NAME", default="Auth Service (UAT)")
WEBAUTHN_ORIGIN = config("WEBAUTHN_ORIGIN", default="https://uat.example.com")

# Security settings for UAT
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=3600, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True, cast=bool
)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
