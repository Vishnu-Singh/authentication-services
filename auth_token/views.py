import base64
import hashlib
import hmac

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from auth_core.models import APIKey, AuthenticationLog


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_api_key(request):
    """
    Create a new API key for the authenticated user.
    """
    name = request.data.get("name", "Default API Key")
    expires_at = request.data.get("expires_at")

    api_key = APIKey.objects.create(user=request.user, name=name, expires_at=expires_at)

    return Response(
        {
            "message": "API key created successfully",
            "api_key": {
                "id": api_key.id,
                "name": api_key.name,
                "key": api_key.key,
                "created_at": api_key.created_at,
                "expires_at": api_key.expires_at,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_api_keys(request):
    """
    List all API keys for the authenticated user.
    """
    api_keys = APIKey.objects.filter(user=request.user)

    return Response(
        {
            "api_keys": [
                {
                    "id": key.id,
                    "name": key.name,
                    "key": key.key[:8] + "...",  # Show only first 8 chars for security
                    "is_active": key.is_active,
                    "created_at": key.created_at,
                    "last_used": key.last_used,
                    "expires_at": key.expires_at,
                }
                for key in api_keys
            ]
        }
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def revoke_api_key(request, key_id):
    """
    Revoke/delete an API key.
    """
    try:
        api_key = APIKey.objects.get(id=key_id, user=request.user)
        api_key.delete()
        return Response({"message": "API key revoked successfully"})
    except APIKey.DoesNotExist:
        return Response(
            {"error": "API key not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_api_key(request):
    """
    Verify an API key and return user information.
    Header: X-API-Key: <api_key>
    """
    api_key_value = request.META.get("HTTP_X_API_KEY")

    if not api_key_value:
        return Response(
            {"error": "API key not provided"}, status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        api_key = APIKey.objects.get(key=api_key_value)

        if not api_key.is_valid():
            return Response(
                {"error": "API key is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Update last used timestamp
        api_key.last_used = timezone.now()
        api_key.save(update_fields=["last_used"])

        # Log authentication
        AuthenticationLog.objects.create(
            user=api_key.user,
            auth_method="api_key",
            success=True,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            details={"api_key_id": api_key.id},
        )

        return Response(
            {
                "valid": True,
                "user": {
                    "id": api_key.user.id,
                    "username": api_key.user.username,
                    "email": api_key.user.email,
                },
            }
        )

    except APIKey.DoesNotExist:
        AuthenticationLog.objects.create(
            user=None,
            auth_method="api_key",
            success=False,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            details={"error": "Invalid API key"},
        )

        return Response(
            {"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_hmac(request):
    """
    Verify HMAC signed request.
    Headers:
        X-Signature: <hmac_signature>
        X-Timestamp: <timestamp>
    """
    signature = request.META.get("HTTP_X_SIGNATURE")
    timestamp = request.META.get("HTTP_X_TIMESTAMP")
    api_key_value = request.META.get("HTTP_X_API_KEY")

    if not all([signature, timestamp, api_key_value]):
        return Response(
            {"error": "Missing required headers"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        api_key = APIKey.objects.get(key=api_key_value)

        if not api_key.is_valid():
            return Response(
                {"error": "API key is invalid or expired"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Verify HMAC signature
        body = request.body.decode("utf-8")
        message = f"{timestamp}{body}"
        expected_signature = hmac.new(
            api_key.key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        if hmac.compare_digest(signature, expected_signature):
            return Response({"valid": True, "message": "HMAC signature verified"})
        else:
            return Response(
                {"error": "Invalid HMAC signature"}, status=status.HTTP_401_UNAUTHORIZED
            )

    except APIKey.DoesNotExist:
        return Response(
            {"error": "Invalid API key"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def basic_auth(request):
    """
    HTTP Basic Authentication endpoint.
    Header: Authorization: Basic <base64(username:password)>
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")

    if not auth_header.startswith("Basic "):
        return Response(
            {"error": "Invalid authorization header"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)

        user = authenticate(username=username, password=password)

        # Log authentication attempt
        AuthenticationLog.objects.create(
            user=user,
            auth_method="basic",
            success=user is not None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            details={"username": username},
        )

        if user is not None:
            return Response(
                {
                    "authenticated": True,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    except (ValueError, IndexError):
        return Response(
            {"error": "Invalid authorization header format"},
            status=status.HTTP_400_BAD_REQUEST,
        )
