"""
Nox configuration for authentication-services project.

This file defines sessions for different environments:
- dev: Development environment
- uat: User Acceptance Testing environment
- prod: Production environment

Usage:
    nox -s dev-install          # Install dependencies for dev
    nox -s dev-test             # Run tests in dev environment
    nox -s dev-migrate          # Run migrations in dev environment
    nox -s dev-server           # Start development server
    nox -s uat-install          # Install dependencies for UAT
    nox -s uat-test             # Run tests in UAT environment
    nox -s prod-install         # Install dependencies for production
    nox -s lint                 # Run linting checks
    nox -s format               # Format code
"""

import nox

# Python version to use
PYTHON_VERSION = "3.12"

# Environment-specific settings modules
ENVIRONMENTS = {
    "dev": "auth_service.settings_dev",
    "uat": "auth_service.settings_uat",
    "prod": "auth_service.settings_prod",
}


@nox.session(python=PYTHON_VERSION, name="dev-install")
def dev_install(session):
    """Install dependencies for development environment."""
    session.install("-r", "requirements.txt")
    session.install(
        "pytest", "pytest-django", "factory-boy", "black", "flake8", "isort"
    )
    session.notify("dev-migrate")


@nox.session(python=PYTHON_VERSION, name="uat-install")
def uat_install(session):
    """Install dependencies for UAT environment."""
    session.install("-r", "requirements.txt")
    session.install("pytest", "pytest-django", "factory-boy")
    session.notify("uat-migrate")


@nox.session(python=PYTHON_VERSION, name="prod-install")
def prod_install(session):
    """Install dependencies for production environment."""
    session.install("-r", "requirements.txt")
    session.install("gunicorn", "psycopg2-binary")


@nox.session(python=PYTHON_VERSION, name="dev-test")
def dev_test(session):
    """Run tests in development environment."""
    session.install("-r", "requirements.txt")
    session.install("pytest", "pytest-django", "factory-boy")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("pytest", ".", "-v", "--tb=short")


@nox.session(python=PYTHON_VERSION, name="uat-test")
def uat_test(session):
    """Run tests in UAT environment."""
    session.install("-r", "requirements.txt")
    session.install("pytest", "pytest-django", "factory-boy")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["uat"]
    session.run("pytest", ".", "-v", "--tb=short")


@nox.session(python=PYTHON_VERSION, name="prod-test")
def prod_test(session):
    """Run tests in production environment (dry-run only)."""
    session.install("-r", "requirements.txt")
    session.install("pytest", "pytest-django", "factory-boy")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["prod"]
    session.run("pytest", ".", "-v", "--tb=short", "-k", "not integration")


@nox.session(python=PYTHON_VERSION, name="dev-migrate")
def dev_migrate(session):
    """Run database migrations for development environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("python", "manage.py", "migrate", "--noinput")


@nox.session(python=PYTHON_VERSION, name="uat-migrate")
def uat_migrate(session):
    """Run database migrations for UAT environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["uat"]
    session.run("python", "manage.py", "migrate", "--noinput")


@nox.session(python=PYTHON_VERSION, name="prod-migrate")
def prod_migrate(session):
    """Run database migrations for production environment."""
    session.install("-r", "requirements.txt")
    session.install("psycopg2-binary")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["prod"]
    session.run("python", "manage.py", "migrate", "--noinput")


@nox.session(python=PYTHON_VERSION, name="dev-server")
def dev_server(session):
    """Start the development server."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("python", "manage.py", "runserver", "0.0.0.0:8000")


@nox.session(python=PYTHON_VERSION, name="uat-server")
def uat_server(session):
    """Start the UAT server."""
    session.install("-r", "requirements.txt")
    session.install("gunicorn")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["uat"]
    session.run(
        "gunicorn",
        "auth_service.wsgi:application",
        "--bind",
        "0.0.0.0:8000",
        "--workers",
        "3",
    )


@nox.session(python=PYTHON_VERSION, name="prod-server")
def prod_server(session):
    """Start the production server."""
    session.install("-r", "requirements.txt")
    session.install("gunicorn", "psycopg2-binary")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["prod"]
    session.run(
        "gunicorn",
        "auth_service.wsgi:application",
        "--bind",
        "0.0.0.0:8000",
        "--workers",
        "4",
    )


@nox.session(python=PYTHON_VERSION, name="dev-shell")
def dev_shell(session):
    """Open Django shell for development environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("python", "manage.py", "shell")


@nox.session(python=PYTHON_VERSION, name="lint")
def lint(session):
    """Run linting checks with flake8."""
    session.install("flake8", "flake8-docstrings")
    session.run(
        "flake8",
        ".",
        "--exclude",
        ".nox,venv,migrations,__pycache__",
        "--max-line-length",
        "120",
        "--ignore",
        "D100,D101,D102,D103,D104,D105,D106,D107",
    )


@nox.session(python=PYTHON_VERSION, name="format")
def format_code(session):
    """Format code with black and isort."""
    session.install("black", "isort")
    session.run("black", ".", "--exclude", r"/(\.nox|venv|migrations|__pycache__)/")
    session.run(
        "isort",
        ".",
        "--skip",
        ".nox",
        "--skip",
        "venv",
        "--skip",
        "migrations",
        "--skip",
        "__pycache__",
    )


@nox.session(python=PYTHON_VERSION, name="format-check")
def format_check(session):
    """Check code formatting without making changes."""
    session.install("black", "isort")
    session.run(
        "black", ".", "--check", "--exclude", r"/(\.nox|venv|migrations|__pycache__)/"
    )
    session.run(
        "isort",
        ".",
        "--check-only",
        "--skip",
        ".nox",
        "--skip",
        "venv",
        "--skip",
        "migrations",
        "--skip",
        "__pycache__",
    )


@nox.session(python=PYTHON_VERSION, name="dev-createsuperuser")
def dev_createsuperuser(session):
    """Create a superuser for development environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("python", "manage.py", "createsuperuser")


@nox.session(python=PYTHON_VERSION, name="dev-collectstatic")
def dev_collectstatic(session):
    """Collect static files for development environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["dev"]
    session.run("python", "manage.py", "collectstatic", "--noinput")


@nox.session(python=PYTHON_VERSION, name="uat-collectstatic")
def uat_collectstatic(session):
    """Collect static files for UAT environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["uat"]
    session.run("python", "manage.py", "collectstatic", "--noinput")


@nox.session(python=PYTHON_VERSION, name="prod-collectstatic")
def prod_collectstatic(session):
    """Collect static files for production environment."""
    session.install("-r", "requirements.txt")
    session.env["DJANGO_SETTINGS_MODULE"] = ENVIRONMENTS["prod"]
    session.run("python", "manage.py", "collectstatic", "--noinput")


@nox.session(python=PYTHON_VERSION, name="clean")
def clean(session):
    """Clean up generated files and caches."""
    import os
    import shutil

    dirs_to_remove = [
        ".nox",
        "__pycache__",
        ".pytest_cache",
        "staticfiles",
        "*.egg-info",
    ]
    for dir_pattern in dirs_to_remove:
        if "*" in dir_pattern:
            # Handle glob patterns
            import glob

            for path in glob.glob(f"**/{dir_pattern}", recursive=True):
                if os.path.exists(path):
                    session.log(f"Removing {path}")
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
        else:
            if os.path.exists(dir_pattern):
                session.log(f"Removing {dir_pattern}")
                shutil.rmtree(dir_pattern)
