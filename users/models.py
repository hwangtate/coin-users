from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import UserManager


class SocialProvider(models.TextChoices):
    GOOGLE = "google", "Google"
    BINANCE = "binance", "Binance"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    social_provider = models.CharField(
        max_length=10, choices=SocialProvider.choices, default=None, null=True, blank=True
    )
    ranking = models.PositiveIntegerField(default=None, null=True, blank=True)

    email_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
