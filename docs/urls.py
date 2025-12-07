from django.urls import path

from . import views

urlpatterns = [
    # API Documentation Endpoints (JSON)
    path("", views.docs_home, name="docs_home"),
    path("setup/", views.setup_guide, name="docs_setup"),
    path("api/", views.api_documentation, name="docs_api"),
    path("changelog/", views.changelog, name="docs_changelog"),
    path("architecture/", views.architecture_docs, name="docs_architecture"),
    path("deployment/", views.deployment_guide, name="docs_deployment"),
    # Web Documentation Pages (HTML)
    path("web/", views.docs_web_home, name="docs_web_home"),
    path("web/setup/", views.docs_web_setup, name="docs_web_setup"),
    path("web/api/", views.docs_web_api, name="docs_web_api"),
    path("web/changelog/", views.docs_web_changelog, name="docs_web_changelog"),
]
