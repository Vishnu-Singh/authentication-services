"""
Development environment settings for auth_service project.

This module extends the base settings with development-specific configurations.
"""

import os
from pathlib import Path
from .settings import *

# Development mode
DEBUG = True

# Environment indicator
ENVIRONMENT = 'development'

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_dev.sqlite3',
    }
}

# CORS - Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Session Configuration - Relaxed for development
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF Configuration - Relaxed for development
CSRF_COOKIE_SECURE = False

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_dev'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_dev'

# Email backend - Console output for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Development-specific JWT settings
from datetime import timedelta
SIMPLE_JWT.update({
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),  # Longer for development
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
})

# WebAuthn settings for development
WEBAUTHN_RP_ID = 'localhost'
WEBAUTHN_RP_NAME = 'Auth Service (Dev)'
WEBAUTHN_ORIGIN = 'http://localhost:8000'

# Show detailed error pages
DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

# Enable Django Debug Toolbar if installed
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
except ImportError:
    pass

# Print SQL queries in console (optional - can be noisy)
# LOGGING['loggers']['django.db.backends'] = {
#     'handlers': ['console'],
#     'level': 'DEBUG',
# }
