import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class APIKey(models.Model):
    """Model for API key based authentication"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "api_keys"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(48)

    def is_valid(self):
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True


class OAuthClient(models.Model):
    """Model for OAuth 2.0 clients"""

    client_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=255)
    client_name = models.CharField(max_length=200)
    redirect_uris = models.TextField(help_text="One per line")
    allowed_scopes = models.TextField(default="openid profile email")
    is_confidential = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "oauth_clients"

    def __str__(self):
        return self.client_name


class SAMLServiceProvider(models.Model):
    """Model for SAML Service Providers"""

    entity_id = models.CharField(max_length=255, unique=True)
    metadata_url = models.URLField(blank=True)
    acs_url = models.URLField(help_text="Assertion Consumer Service URL")
    slo_url = models.URLField(blank=True, help_text="Single Logout URL")
    certificate = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "saml_service_providers"

    def __str__(self):
        return self.entity_id


class RoutingRule(models.Model):
    """Model for request routing configuration"""

    name = models.CharField(max_length=100)
    source_path = models.CharField(max_length=255, help_text="Path pattern to match")
    target_url = models.URLField(help_text="Target endpoint URL")
    auth_method = models.CharField(
        max_length=50,
        choices=[
            ("session", "Session"),
            ("jwt", "JWT Token"),
            ("oauth", "OAuth 2.0"),
            ("saml", "SAML"),
            ("api_key", "API Key"),
            ("basic", "HTTP Basic"),
            ("mtls", "mTLS"),
        ],
        default="session",
    )
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "routing_rules"
        ordering = ["priority", "-created_at"]

    def __str__(self):
        return f"{self.name}: {self.source_path} -> {self.target_url}"


class AuthenticationLog(models.Model):
    """Model for logging authentication attempts"""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    auth_method = models.CharField(max_length=50)
    success = models.BooleanField()
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "authentication_logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["auth_method", "timestamp"]),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        status = "Success" if self.success else "Failed"
        return f"{user_str} - {self.auth_method} - {status}"
