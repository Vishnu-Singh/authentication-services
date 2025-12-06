from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from datetime import timedelta


class MagicLink(models.Model):
    """Model for magic link passwordless authentication"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magic_links')
    token = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    
    class Meta:
        db_table = 'magic_links'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Magic link for {self.email}"
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_urlsafe(48)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        if self.is_used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True


class OneTimeCode(models.Model):
    """Model for one-time codes sent via email/SMS"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=10)
    delivery_method = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('sms', 'SMS')],
        default='email'
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'one_time_codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_code(length=6):
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    
    def is_valid(self):
        if self.is_used:
            return False
        if self.attempts >= 3:  # Max 3 attempts
            return False
        if timezone.now() > self.expires_at:
            return False
        return True

