"""
Chat 앱의 URL 패턴을 정의하는 모듈입니다.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"rooms", ChatRoomViewSet, basename="chatroom")

message_router = DefaultRouter()
message_router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path("rooms/<int:room_pk>/", include(message_router.urls)),
]
