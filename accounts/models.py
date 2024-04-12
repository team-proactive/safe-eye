# accounts/models.py
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from utils.models import Status, Tag


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, password=None, nickname=None, role="user", **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, nickname=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(
            email, password, nickname, role="superuser", **extra_fields
        )


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self):
        import uuid

        return str(uuid.uuid4())
