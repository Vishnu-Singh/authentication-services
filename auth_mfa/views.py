import base64
import io

import pyotp
import qrcode
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from auth_mfa.models import BackupCode, TOTPDevice, WebAuthnCredential


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def setup_totp(request):
    """
    Setup TOTP (Time-based One-Time Password) for 2FA.
    Returns secret and QR code for authenticator app.
    """
    device, created = TOTPDevice.objects.get_or_create(user=request.user)

    if not created and device.is_confirmed:
        return Response(
            {"error": "TOTP already configured. Disable it first to reconfigure."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Generate provisioning URI for QR code
    totp = pyotp.TOTP(device.secret)
    provisioning_uri = totp.provisioning_uri(
        name=request.user.username, issuer_name="Auth Service"
    )

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return Response(
        {
            "secret": device.secret,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "provisioning_uri": provisioning_uri,
            "message": "Scan the QR code with your authenticator app and verify with a code",
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_totp(request):
    """
    Verify TOTP code to enable 2FA.
    """
    code = request.data.get("code")

    if not code:
        return Response(
            {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        device = TOTPDevice.objects.get(user=request.user)
        totp = pyotp.TOTP(device.secret)

        if totp.verify(code, valid_window=1):
            device.is_confirmed = True
            device.last_used = timezone.now()
            device.save()

            # Generate backup codes
            backup_codes = []
            for _ in range(10):
                backup_code = BackupCode.objects.create(
                    user=request.user, code=BackupCode.generate_code()
                )
                backup_codes.append(backup_code.code)

            return Response(
                {
                    "message": "TOTP enabled successfully",
                    "backup_codes": backup_codes,
                    "note": "Save these backup codes in a safe place",
                }
            )
        else:
            return Response(
                {"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
            )

    except TOTPDevice.DoesNotExist:
        return Response(
            {"error": "TOTP not configured. Call setup-totp first."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def validate_totp(request):
    """
    Validate TOTP code during login.
    """
    username = request.data.get("username")
    code = request.data.get("code")

    if not username or not code:
        return Response(
            {"error": "username and code are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        from django.contrib.auth.models import User

        user = User.objects.get(username=username)
        device = TOTPDevice.objects.get(user=user, is_confirmed=True)

        totp = pyotp.TOTP(device.secret)

        if totp.verify(code, valid_window=1):
            device.last_used = timezone.now()
            device.save()

            return Response(
                {"valid": True, "message": "TOTP code validated successfully"}
            )
        else:
            # Try backup codes
            backup_code = BackupCode.objects.filter(
                user=user, code=code, is_used=False
            ).first()

            if backup_code:
                backup_code.is_used = True
                backup_code.used_at = timezone.now()
                backup_code.save()

                return Response(
                    {
                        "valid": True,
                        "message": "Backup code validated successfully",
                        "warning": "This backup code has been used and cannot be used again",
                    }
                )

            return Response(
                {"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST
            )

    except (User.DoesNotExist, TOTPDevice.DoesNotExist):
        return Response(
            {"error": "TOTP not configured for this user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def disable_totp(request):
    """
    Disable TOTP 2FA for the user.
    """
    try:
        device = TOTPDevice.objects.get(user=request.user)
        device.delete()

        # Delete backup codes
        BackupCode.objects.filter(user=request.user).delete()

        return Response({"message": "TOTP disabled successfully"})

    except TOTPDevice.DoesNotExist:
        return Response(
            {"error": "TOTP not configured"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_webauthn(request):
    """
    Register a WebAuthn/FIDO2 credential (passkey, security key).
    """
    credential_id = request.data.get("credential_id")
    public_key = request.data.get("public_key")
    name = request.data.get("name", "Security Key")

    if not credential_id or not public_key:
        return Response(
            {"error": "credential_id and public_key are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    credential = WebAuthnCredential.objects.create(
        user=request.user, credential_id=credential_id, public_key=public_key, name=name
    )

    return Response(
        {
            "message": "WebAuthn credential registered successfully",
            "credential": {
                "id": credential.id,
                "name": credential.name,
                "created_at": credential.created_at,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_webauthn(request):
    """
    List all WebAuthn credentials for the user.
    """
    credentials = WebAuthnCredential.objects.filter(user=request.user)

    return Response(
        {
            "credentials": [
                {
                    "id": cred.id,
                    "name": cred.name,
                    "created_at": cred.created_at,
                    "last_used": cred.last_used,
                }
                for cred in credentials
            ]
        }
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_webauthn(request, credential_id):
    """
    Delete a WebAuthn credential.
    """
    try:
        credential = WebAuthnCredential.objects.get(id=credential_id, user=request.user)
        credential.delete()

        return Response({"message": "WebAuthn credential deleted successfully"})

    except WebAuthnCredential.DoesNotExist:
        return Response(
            {"error": "Credential not found"}, status=status.HTTP_404_NOT_FOUND
        )
