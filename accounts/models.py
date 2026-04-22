from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)  # E.164 max is 15 digits

    is_verified = models.BooleanField(default=False)

    # Use email as the login credential instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    full_name = models.CharField(max_length=100)  # 25 is too short for many names
    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


OTP_EXPIRY_MINUTES = 10


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_used"]),  # speeds up unused-OTP lookups
        ]

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.created_at + timedelta(minutes=OTP_EXPIRY_MINUTES)

    @property
    def is_valid(self) -> bool:
        return not self.is_used and not self.is_expired

    def __str__(self):
        return f"{self.user.email} - {self.code}"