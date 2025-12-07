# Nox Setup Summary

This document provides a summary of the Nox configuration implemented for the authentication-services project.

## Overview

Nox has been configured to manage three distinct environments:

1. **Development (dev)** - For local development
2. **User Acceptance Testing (UAT)** - For staging/testing
3. **Production (prod)** - For production deployment

## Files Added

### Configuration Files

- **noxfile.py** - Main Nox configuration with 21 sessions
- **auth_service/settings_dev.py** - Development environment settings
- **auth_service/settings_uat.py** - UAT environment settings
- **auth_service/settings_prod.py** - Production environment settings

### Environment Templates

- **.env.dev** - Development environment variables template
- **.env.uat** - UAT environment variables template
- **.env.prod** - Production environment variables template

### Documentation

- **NOX_GUIDE.md** - Comprehensive guide for using Nox
- **quickstart.sh** - Interactive script for quick environment setup

## Available Nox Sessions

### Installation Sessions (3)
- `dev-install` - Install dependencies for development
- `uat-install` - Install dependencies for UAT
- `prod-install` - Install dependencies for production

### Testing Sessions (3)
- `dev-test` - Run tests in development environment
- `uat-test` - Run tests in UAT environment
- `prod-test` - Run tests in production environment (excludes integration tests)

### Migration Sessions (3)
- `dev-migrate` - Run database migrations for development
- `uat-migrate` - Run database migrations for UAT
- `prod-migrate` - Run database migrations for production

### Server Sessions (3)
- `dev-server` - Start Django development server
- `uat-server` - Start Gunicorn server with 3 workers
- `prod-server` - Start Gunicorn server with 4 workers

### Code Quality Sessions (3)
- `lint` - Run flake8 linting checks
- `format` - Format code with black and isort
- `format-check` - Check code formatting without changes

### Utility Sessions (6)
- `dev-shell` - Open Django shell in development
- `dev-createsuperuser` - Create superuser in development
- `dev-collectstatic` - Collect static files for development
- `uat-collectstatic` - Collect static files for UAT
- `prod-collectstatic` - Collect static files for production
- `clean` - Clean up generated files and caches

## Environment Differences

### Development Environment
- **Debug Mode**: Enabled
- **Database**: SQLite (db_dev.sqlite3)
- **Email**: Console backend (prints to terminal)
- **Security**: Relaxed settings for local development
- **JWT Tokens**: 2-hour access, 7-day refresh
- **CORS**: Allows all origins
- **Logging**: DEBUG level with console output

### UAT Environment
- **Debug Mode**: Configurable (default: disabled)
- **Database**: PostgreSQL/MySQL recommended
- **Email**: SMTP backend
- **Security**: Moderate security with HTTPS
- **JWT Tokens**: 60-minute access, 1-day refresh
- **CORS**: Restricted origins (configurable)
- **Logging**: INFO level with file and console output

### Production Environment
- **Debug Mode**: Disabled (enforced)
- **Database**: PostgreSQL/MySQL required
- **Email**: SMTP backend
- **Security**: Maximum security settings with HSTS
- **JWT Tokens**: 15-minute access, 12-hour refresh
- **CORS**: Strict origin control
- **Logging**: WARNING level with file, console, and email alerts
- **Caching**: Redis recommended

## Quick Start Examples

### Development Environment
```bash
# Quick setup with script
./quickstart.sh dev

# Manual setup
cp .env.dev .env
nox -s dev-install
nox -s dev-createsuperuser
nox -s dev-server
```

### UAT Environment
```bash
# Setup
cp .env.uat .env
# Edit .env with UAT configuration
nox -s uat-install
nox -s uat-migrate
nox -s uat-collectstatic
nox -s uat-test
nox -s uat-server
```

### Production Environment
```bash
# Setup
cp .env.prod .env
# Edit .env with production configuration
nox -s prod-install
nox -s prod-migrate
nox -s prod-collectstatic
nox -s prod-test
nox -s prod-server
```

## Benefits

1. **Environment Isolation**: Each environment has its own isolated virtual environment
2. **Consistent Setup**: Same commands work across all environments
3. **Reduced Errors**: Automated setup reduces configuration mistakes
4. **Easy Testing**: Quick environment switching for testing
5. **Documentation**: Self-documenting configuration in noxfile.py
6. **Reproducibility**: Consistent builds across different machines

## Dependencies Added

- **nox>=2023.4.22** - Task automation tool
- **black>=23.12.0** - Code formatter
- **flake8>=7.0.0** - Linting tool
- **isort>=5.13.0** - Import sorting tool

## Security Considerations

### Development
- Debug mode enabled for troubleshooting
- Console email backend (no real emails sent)
- Relaxed CORS for frontend development
- SQLite database for simplicity

### UAT
- Debug mode disabled by default
- HTTPS enforcement configurable
- Restricted CORS origins
- PostgreSQL recommended
- Moderate security headers

### Production
- Debug mode always disabled
- HTTPS with HSTS enforced
- Strict CORS policy
- PostgreSQL/MySQL required
- Maximum security headers
- Redis caching for performance
- Error email notifications

## Integration with CI/CD

Nox sessions can be easily integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Tests
  run: nox -s uat-test

- name: Lint Code
  run: nox -s lint

- name: Check Formatting
  run: nox -s format-check
```

## Maintenance

### Updating Dependencies
1. Update requirements.txt
2. Run `nox -s <env>-install` to update environment

### Cleaning Up
```bash
nox -s clean  # Remove all .nox directories and caches
```

### Adding New Sessions
Edit `noxfile.py` to add new sessions following the existing pattern.

## Support

For detailed usage instructions, refer to:
- **NOX_GUIDE.md** - Complete Nox usage guide
- **README.md** - Project setup instructions
- Run `nox --list` - List all available sessions
- Run `nox -s <session> --help` - Get help for a specific session

## Version Information

- **Nox Version**: 2023.4.22+
- **Python Version**: 3.12 (configurable in noxfile.py)
- **Django Version**: 6.0
