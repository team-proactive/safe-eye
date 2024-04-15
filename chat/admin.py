"""
Chat 앱의 관리자 페이지 설정을 정의하는 모듈입니다.
"""

from django.contrib import admin
from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "sender", "content", "timestamp")
    list_filter = ("room", "sender", "timestamp")
    search_fields = ("content",)
