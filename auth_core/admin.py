from django.contrib import admin
from .models import APIKey, OAuthClient, SAMLServiceProvider, RoutingRule, AuthenticationLog


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'created_at', 'last_used', 'expires_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username', 'key']
    readonly_fields = ['key', 'created_at', 'last_used']


@admin.register(OAuthClient)
class OAuthClientAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_id', 'is_confidential', 'is_active', 'created_at']
    list_filter = ['is_confidential', 'is_active', 'created_at']
    search_fields = ['client_name', 'client_id']


@admin.register(SAMLServiceProvider)
class SAMLServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['entity_id', 'acs_url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['entity_id']


@admin.register(RoutingRule)
class RoutingRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'source_path', 'target_url', 'auth_method', 'priority', 'is_active']
    list_filter = ['auth_method', 'is_active']
    search_fields = ['name', 'source_path', 'target_url']


@admin.register(AuthenticationLog)
class AuthenticationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'auth_method', 'success', 'ip_address', 'timestamp']
    list_filter = ['auth_method', 'success', 'timestamp']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'auth_method', 'success', 'ip_address', 'user_agent', 'timestamp', 'details']

