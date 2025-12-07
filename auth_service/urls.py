"""
URL configuration for auth_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT Token endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Authentication app endpoints
    path("api/auth/session/", include("auth_session.urls")),
    path("api/auth/token/", include("auth_token.urls")),
    path("api/auth/oauth/", include("auth_oauth.urls")),
    path("api/auth/saml/", include("auth_saml.urls")),
    path("api/auth/mfa/", include("auth_mfa.urls")),
    path("api/auth/passwordless/", include("auth_passwordless.urls")),
    # API routing endpoint
    path("api/route/", include("auth_api_routing.urls")),
    # Documentation endpoints
    path("api/docs/", include("docs.urls")),
]
