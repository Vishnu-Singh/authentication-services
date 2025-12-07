from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_core.models import AuthenticationLog, OAuthClient


@api_view(["GET"])
@permission_classes([AllowAny])
def oauth_authorize(request):
    """
    OAuth 2.0 Authorization endpoint.
    Implements the authorization code flow.
    """
    client_id = request.GET.get("client_id")
    redirect_uri = request.GET.get("redirect_uri")
    response_type = request.GET.get("response_type", "code")
    scope = request.GET.get("scope", "openid profile email")
    state = request.GET.get("state", "")

    if not client_id or not redirect_uri:
        return Response(
            {"error": "client_id and redirect_uri are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        client = OAuthClient.objects.get(client_id=client_id, is_active=True)

        # Verify redirect URI
        allowed_uris = client.redirect_uris.split("\n")
        if redirect_uri not in allowed_uris:
            return Response(
                {"error": "Invalid redirect_uri"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Authorization request received",
                "client_name": client.client_name,
                "scope": scope,
                "redirect_uri": redirect_uri,
                "state": state,
                "note": "In production, this would redirect to login/consent page",
            }
        )

    except OAuthClient.DoesNotExist:
        return Response(
            {"error": "Invalid client_id"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def oauth_token(request):
    """
    OAuth 2.0 Token endpoint.
    Exchange authorization code for access token.
    """
    grant_type = request.data.get("grant_type")
    code = request.data.get("code")
    client_id = request.data.get("client_id")
    client_secret = request.data.get("client_secret")
    redirect_uri = request.data.get("redirect_uri")

    if grant_type != "authorization_code":
        return Response(
            {"error": "unsupported_grant_type"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not all([code, client_id, client_secret, redirect_uri]):
        return Response(
            {"error": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        client = OAuthClient.objects.get(
            client_id=client_id, client_secret=client_secret, is_active=True
        )

        # In production, verify the authorization code
        # For now, return a mock response
        return Response(
            {
                "access_token": "mock_access_token_" + code,
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "mock_refresh_token",
                "scope": "openid profile email",
                "note": "This is a mock implementation. Integrate with OAuth toolkit in production.",
            }
        )

    except OAuthClient.DoesNotExist:
        return Response(
            {"error": "invalid_client"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def oidc_discovery(request):
    """
    OpenID Connect Discovery endpoint.
    Returns the OpenID Connect configuration.
    """
    base_url = request.build_absolute_uri("/")[:-1]

    return Response(
        {
            "issuer": base_url,
            "authorization_endpoint": f"{base_url}/api/auth/oauth/authorize/",
            "token_endpoint": f"{base_url}/api/auth/oauth/token/",
            "userinfo_endpoint": f"{base_url}/api/auth/oauth/userinfo/",
            "jwks_uri": f"{base_url}/api/auth/oauth/jwks/",
            "response_types_supported": ["code", "token", "id_token"],
            "subject_types_supported": ["public"],
            "id_token_signing_alg_values_supported": ["RS256"],
            "scopes_supported": ["openid", "profile", "email"],
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def oauth_userinfo(request):
    """
    OAuth 2.0 / OIDC UserInfo endpoint.
    Returns information about the authenticated user.
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")

    if not auth_header.startswith("Bearer "):
        return Response(
            {"error": "Missing or invalid authorization header"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # In production, verify the access token
    # For now, return mock data if user is authenticated
    if request.user.is_authenticated:
        return Response(
            {
                "sub": str(request.user.id),
                "name": f"{request.user.first_name} {request.user.last_name}",
                "preferred_username": request.user.username,
                "email": request.user.email,
                "email_verified": True,
            }
        )
    else:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def social_login(request):
    """
    Social/Federated login endpoint.
    Supports Google, GitHub, Facebook, etc.
    """
    provider = request.data.get("provider")
    access_token = request.data.get("access_token")

    if not provider or not access_token:
        return Response(
            {"error": "provider and access_token are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # In production, verify the access token with the social provider
    # and create/update user account

    return Response(
        {
            "message": f"{provider} login initiated",
            "note": "Integrate with social-auth-app-django for production use",
            "supported_providers": [
                "google",
                "github",
                "facebook",
                "twitter",
                "linkedin",
            ],
        }
    )
