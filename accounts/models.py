# accounts/models.py
"""
이 모듈은 Django 모델을 정의합니다.
CustomUser 모델과 UserToken 모델이 포함되어 있습니다.
"""

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
    """
    CustomUser 모델에 대한 사용자 관리 클래스입니다.
    """

    def _create_user(self, email, password, nickname, role, **extra_fields):
        """
        새로운 CustomUser 인스턴스를 생성합니다.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, nickname, role="user", **extra_fields):
        """
        새로운 일반 사용자를 생성합니다.
        """
        return self._create_user(email, password, nickname, role, **extra_fields)

    def create_superuser(self, email, password, nickname, **extra_fields):
        """
        새로운 슈퍼 사용자를 생성합니다.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, nickname, "superuser", **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    사용자 정보를 저장하는 모델입니다.
    """

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
    """
    사용자 토큰 정보를 저장하는 모델입니다.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    token = models.CharField(max_length=255, unique=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        토큰을 저장할 때 토큰 값을 생성합니다.
        """
        if not self.token:
            refresh = RefreshToken.for_user(self.user)
            self.token = str(refresh)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.token
