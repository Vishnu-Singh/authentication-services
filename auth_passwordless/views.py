from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_core.models import AuthenticationLog
from auth_passwordless.models import MagicLink, OneTimeCode


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(["POST"])
@permission_classes([AllowAny])
def request_magic_link(request):
    """
    Request a magic link for passwordless authentication.
    Sends an email with a magic link to the user.
    """
    email = request.data.get("email")

    if not email:
        return Response(
            {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

        # Create magic link
        magic_link = MagicLink.objects.create(
            user=user, email=email, ip_address=get_client_ip(request)
        )

        # In production, send email with magic link
        magic_link_url = request.build_absolute_uri(
            f"/api/auth/passwordless/magic-link/verify/?token={magic_link.token}"
        )

        return Response(
            {
                "message": "Magic link sent to your email",
                "magic_link": magic_link_url,  # Remove in production
                "expires_in": "15 minutes",
                "note": "In production, this would send an email. For testing, the link is included above.",
            }
        )

    except User.DoesNotExist:
        # Don't reveal if email exists
        return Response(
            {"message": "If this email is registered, a magic link has been sent"}
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def verify_magic_link(request):
    """
    Verify magic link token and authenticate user.
    """
    token = request.GET.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        magic_link = MagicLink.objects.get(token=token)

        if not magic_link.is_valid():
            return Response(
                {"error": "Magic link has expired or been used"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark as used
        magic_link.is_used = True
        magic_link.used_at = timezone.now()
        magic_link.save()

        # Log authentication
        AuthenticationLog.objects.create(
            user=magic_link.user,
            auth_method="magic_link",
            success=True,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            details={"email": magic_link.email},
        )

        # Authenticate user
        login(
            request,
            magic_link.user,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        return Response(
            {
                "message": "Authentication successful",
                "user": {
                    "id": magic_link.user.id,
                    "username": magic_link.user.username,
                    "email": magic_link.user.email,
                },
            }
        )

    except MagicLink.DoesNotExist:
        return Response(
            {"error": "Invalid magic link"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def request_otp(request):
    """
    Request a one-time code for passwordless authentication.
    Sends OTP via email or SMS.
    """
    email = request.data.get("email")
    delivery_method = request.data.get("method", "email")  # email or sms

    if not email:
        return Response(
            {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if delivery_method not in ["email", "sms"]:
        return Response(
            {"error": 'Invalid delivery method. Use "email" or "sms"'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)

        # Create OTP
        otp = OneTimeCode.objects.create(user=user, delivery_method=delivery_method)

        # In production, send email/SMS with OTP
        return Response(
            {
                "message": f"One-time code sent via {delivery_method}",
                "otp": otp.code,  # Remove in production
                "expires_in": "10 minutes",
                "note": "In production, the OTP would be sent and not returned in response.",
            }
        )

    except User.DoesNotExist:
        # Don't reveal if email exists
        return Response(
            {"message": "If this email is registered, a code has been sent"}
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verify one-time code and authenticate user.
    """
    email = request.data.get("email")
    code = request.data.get("code")

    if not email or not code:
        return Response(
            {"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)

        # Get the most recent valid OTP
        otp = (
            OneTimeCode.objects.filter(user=user, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not otp or not otp.is_valid():
            return Response(
                {"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Increment attempts
        otp.attempts += 1
        otp.save()

        if otp.code != code:
            if otp.attempts >= 3:
                return Response(
                    {"error": "Too many failed attempts. Request a new code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": f"Invalid code. {3 - otp.attempts} attempts remaining."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mark as used
        otp.is_used = True
        otp.used_at = timezone.now()
        otp.save()

        # Log authentication
        AuthenticationLog.objects.create(
            user=user,
            auth_method="otp",
            success=True,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            details={"email": email, "delivery_method": otp.delivery_method},
        )

        # Authenticate user
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        return Response(
            {
                "message": "Authentication successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            }
        )

    except User.DoesNotExist:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
