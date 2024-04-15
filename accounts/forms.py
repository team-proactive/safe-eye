"""
이 모듈은 Django 폼을 정의합니다.
CustomUser 모델과 관련된 폼이 포함되어 있습니다.
"""

# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    새로운 CustomUser 인스턴스를 생성하기 위한 폼입니다.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "nickname", "role")


class CustomUserChangeForm(UserChangeForm):
    """
    기존 CustomUser 인스턴스를 변경하기 위한 폼입니다.
    """

    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "role", "is_active", "is_staff", "is_superuser")
