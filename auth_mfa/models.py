import secrets

from django.contrib.auth.models import User
from django.db import models


class TOTPDevice(models.Model):
    """Model for TOTP (Time-based One-Time Password) devices"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="totp_device"
    )
    secret = models.CharField(max_length=32)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "totp_devices"

    def __str__(self):
        return f"TOTP for {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = secrets.token_hex(16).upper()
        super().save(*args, **kwargs)


class BackupCode(models.Model):
    """Model for backup codes for 2FA"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="backup_codes"
    )
    code = models.CharField(max_length=16, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "backup_codes"

    def __str__(self):
        status = "Used" if self.is_used else "Active"
        return f"Backup code for {self.user.username} ({status})"

    @staticmethod
    def generate_code():
        return secrets.token_hex(8).upper()


class WebAuthnCredential(models.Model):
    """Model for WebAuthn/FIDO2 credentials"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="webauthn_credentials"
    )
    credential_id = models.CharField(max_length=255, unique=True)
    public_key = models.TextField()
    sign_count = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="Security Key")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "webauthn_credentials"

    def __str__(self):
        return f"{self.name} for {self.user.username}"
