from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import Status


class CustomUser(AbstractUser):
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    # 추가 필드
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    profile_status = models.CharField(
        max_length=100,
        choices=[
            ("출동 중", "출동 중"),
            ("대기 중", "대기 중"),
            ("처리 중", "처리 중"),
        ],
        default="대기 중",
    )
    profile_message = models.TextField(blank=True)

    def __str__(self):
        return self.username
