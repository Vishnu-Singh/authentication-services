# Nox Configuration Guide

This project uses [Nox](https://nox.thea.codes/) to manage different environments (dev, UAT, and production) and automate common tasks like testing, linting, and migrations.

## What is Nox?

Nox is a command-line tool that automates testing in multiple Python environments, similar to tox but with a Python configuration file instead of an INI file. It allows you to define sessions for different tasks and environments.

## Installation

Nox is included in the development dependencies. Install it with:

```bash
pip install nox
```

Or install all dependencies including Nox:

```bash
pip install -r requirements.txt
```

## Available Environments

The project is configured to work with three environments:

- **dev**: Development environment (local development, debug enabled)
- **uat**: User Acceptance Testing environment (staging/pre-production)
- **prod**: Production environment (production-ready configuration)

Each environment has its own settings file:
- `auth_service/settings_dev.py`
- `auth_service/settings_uat.py`
- `auth_service/settings_prod.py`

## Environment Configuration

Before using Nox, copy the appropriate environment template:

```bash
# For development
cp .env.dev .env

# For UAT
cp .env.uat .env

# For production
cp .env.prod .env
```

Then edit `.env` to configure your environment-specific settings.

## Available Nox Sessions

### Installation Sessions

Install dependencies for a specific environment:

```bash
# Development environment
nox -s dev-install

# UAT environment
nox -s uat-install

# Production environment
nox -s prod-install
```

### Testing Sessions

Run tests in different environments:

```bash
# Run tests in development
nox -s dev-test

# Run tests in UAT
nox -s uat-test

# Run tests in production (excludes integration tests)
nox -s prod-test
```

### Database Migration Sessions

Run database migrations:

```bash
# Development environment
nox -s dev-migrate

# UAT environment
nox -s uat-migrate

# Production environment
nox -s prod-migrate
```

### Server Sessions

Start the application server:

```bash
# Development server (Django runserver)
nox -s dev-server

# UAT server (Gunicorn with 3 workers)
nox -s uat-server

# Production server (Gunicorn with 4 workers)
nox -s prod-server
```

### Code Quality Sessions

Lint and format code:

```bash
# Run linting checks
nox -s lint

# Format code with black and isort
nox -s format

# Check formatting without changes
nox -s format-check
```

### Utility Sessions

Additional utility commands:

```bash
# Open Django shell in development
nox -s dev-shell

# Create superuser in development
nox -s dev-createsuperuser

# Collect static files for development
nox -s dev-collectstatic

# Collect static files for UAT
nox -s uat-collectstatic

# Collect static files for production
nox -s prod-collectstatic

# Clean up generated files and caches
nox -s clean
```

## Common Workflows

### Setting up Development Environment

```bash
# 1. Copy environment file
cp .env.dev .env

# 2. Install dependencies and run migrations
nox -s dev-install

# 3. Create a superuser
nox -s dev-createsuperuser

# 4. Start the development server
nox -s dev-server
```

### Running Tests

```bash
# Run tests in development
nox -s dev-test

# Run linting
nox -s lint

# Format code
nox -s format
```

### Deploying to UAT

```bash
# 1. Configure UAT environment
cp .env.uat .env
# Edit .env with UAT-specific values

# 2. Install dependencies
nox -s uat-install

# 3. Run migrations
nox -s uat-migrate

# 4. Collect static files
nox -s uat-collectstatic

# 5. Run tests
nox -s uat-test

# 6. Start UAT server
nox -s uat-server
```

### Deploying to Production

```bash
# 1. Configure production environment
cp .env.prod .env
# Edit .env with production values

# 2. Install dependencies
nox -s prod-install

# 3. Run migrations
nox -s prod-migrate

# 4. Collect static files
nox -s prod-collectstatic

# 5. Run production tests
nox -s prod-test

# 6. Start production server (or use systemd/supervisor)
nox -s prod-server
```

## Environment-Specific Features

### Development Environment

- **Debug mode enabled**
- **SQLite database** (db_dev.sqlite3)
- **Console email backend** (emails printed to console)
- **Relaxed security settings**
- **Longer JWT token lifetime** (2 hours access, 7 days refresh)
- **Detailed logging** (DEBUG level)

### UAT Environment

- **Debug mode disabled** (configurable)
- **PostgreSQL/MySQL recommended**
- **SMTP email backend**
- **HTTPS enforced**
- **Moderate security settings**
- **Standard JWT token lifetime** (60 minutes access, 1 day refresh)
- **File and console logging** (INFO level)

### Production Environment

- **Debug mode disabled** (enforced)
- **PostgreSQL/MySQL required**
- **SMTP email backend**
- **Maximum security settings**
- **HTTPS enforced with HSTS**
- **Shorter JWT token lifetime** (15 minutes access, 12 hours refresh)
- **File and console logging with error emails** (WARNING level)
- **Redis caching recommended**

## Tips and Best Practices

1. **Always use the appropriate environment**: Don't run production sessions with dev settings
2. **Keep .env files secure**: Never commit production .env files to version control
3. **Run tests before deployment**: Use `nox -s <env>-test` before deploying
4. **Format code regularly**: Run `nox -s format` before committing
5. **Clean up regularly**: Run `nox -s clean` to remove cache files

## Listing All Sessions

To see all available Nox sessions:

```bash
nox --list
```

To see detailed information about sessions:

```bash
nox --list-sessions
```

## Running Multiple Sessions

You can run multiple sessions in sequence:

```bash
# Format code, lint, and run tests
nox -s format lint dev-test
```

## Troubleshooting

### Session fails with "Python interpreter not found"

Ensure you have Python 3.12 installed, or modify the `PYTHON_VERSION` in `noxfile.py`.

### Database connection errors

Check your `.env` file for correct database configuration.

### Import errors

Ensure all dependencies are installed with the appropriate `*-install` session.

### Permission errors during migration

Ensure your database user has the necessary permissions.

## Additional Resources

- [Nox Documentation](https://nox.thea.codes/)
- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/topics/settings/)
- [python-decouple Documentation](https://github.com/henriquebastos/python-decouple)
