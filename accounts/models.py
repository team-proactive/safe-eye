# accounts/models.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from utils.models import Status, Tag
from django.contrib.auth.models import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, nickname, role, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, nickname, role="user", **extra_fields):
        return self._create_user(email, password, nickname, role, **extra_fields)

    def create_superuser(self, email, password, nickname, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, nickname, "superuser", **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
        ("superuser", "Superuser"),
    )

    admin = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="user", null=True, blank=True
    )

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    user_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    nickname = models.CharField(max_length=255)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default="user")
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.email


class UserToken(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    token = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            refresh = RefreshToken.for_user(self.user)
            self.token = str(refresh)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.token
