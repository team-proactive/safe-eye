"""
이 모듈은 Django 앱 설정을 정의합니다.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Accounts 앱의 설정 클래스입니다.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
