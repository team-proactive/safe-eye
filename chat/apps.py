"""
Chat 앱의 구성을 정의하는 모듈입니다.
"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"
