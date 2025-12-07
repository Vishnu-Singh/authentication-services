# Documentation App

This Django app provides comprehensive documentation for the Authentication Service, including project setup, API reference, and changelog information.

## Features

### JSON API Endpoints

All documentation is available as JSON via REST API:

- **`GET /api/docs/`** - Documentation home with section links
- **`GET /api/docs/setup/`** - Complete setup and installation guide
- **`GET /api/docs/api/`** - Comprehensive API reference for all endpoints
- **`GET /api/docs/changelog/`** - Version history and API changes
- **`GET /api/docs/architecture/`** - System architecture documentation
- **`GET /api/docs/deployment/`** - Production deployment guide

### Web Documentation Pages

Human-friendly HTML documentation:

- **`GET /api/docs/web/`** - Interactive documentation home page
- **`GET /api/docs/web/setup/`** - Web-based setup guide with syntax highlighting
- **`GET /api/docs/web/api/`** - Interactive API reference
- **`GET /api/docs/web/changelog/`** - Formatted changelog

## Usage

### Access JSON Documentation

```bash
# Get all documentation sections
curl http://localhost:8000/api/docs/

# Get setup guide
curl http://localhost:8000/api/docs/setup/

# Get API reference
curl http://localhost:8000/api/docs/api/

# Get changelog
curl http://localhost:8000/api/docs/changelog/
```

### Access Web Documentation

Open your browser and visit:
- http://localhost:8000/api/docs/web/

## Documentation Content

### Setup Guide
- Prerequisites (Python, pip, database)
- Installation steps
- Configuration guide
- Project structure overview
- Quick testing instructions
- Troubleshooting tips

### API Reference
- All authentication methods
- Complete endpoint documentation
- Request/response examples
- Error codes and handling
- Rate limiting information

### Changelog
- Version history
- New features
- Breaking changes
- Bug fixes
- Migration guides
- API versioning strategy

### Architecture
- System overview
- Component descriptions
- Request flow diagrams
- Security layers
- Scalability considerations
- Integration points

### Deployment Guide
- Environment configurations
- Deployment options (traditional, Docker, cloud)
- Configuration checklists
- Security best practices
- Performance optimization
- Monitoring setup
- Backup strategies

## Templates

The web documentation uses Django templates located in `docs/templates/docs/`:

- `base.html` - Base template with styling and navigation
- `home.html` - Documentation home page
- `setup.html` - Setup guide page
- `api.html` - API reference page
- `changelog.html` - Changelog page

## Customization

### Adding New Documentation Sections

1. Add a new view function in `views.py`
2. Add the route in `urls.py`
3. Create a template in `templates/docs/` (for web version)
4. Update the navigation in `base.html`

### Updating Content

Documentation content is defined in the view functions. Update the dictionaries and data structures to modify the documentation.

## Integration

The docs app is automatically integrated into the main Django project:

1. Added to `INSTALLED_APPS` in `settings.py`
2. Routed via `/api/docs/` in main `urls.py`
3. No authentication required - all endpoints are public

## Benefits

- **Version Controlled**: Documentation is part of the codebase
- **Always in Sync**: Documentation updates with code changes
- **Multiple Formats**: Both JSON API and web interface
- **Easy to Navigate**: Clear structure and organization
- **Searchable**: JSON format enables programmatic searching
- **Offline Access**: Available without external dependencies
- **Professional**: Clean, modern web interface

## Future Enhancements

- Add search functionality
- Generate OpenAPI/Swagger specification
- Add interactive API testing (like Swagger UI)
- Code syntax highlighting for examples
- PDF export of documentation
- Versioned documentation (v1, v2, etc.)
