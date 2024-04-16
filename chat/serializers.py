"""
Chat 앱의 시리얼라이저를 정의하는 모듈입니다.
ChatRoomSerializer와 MessageSerializer를 포함하고 있습니다.
"""

from rest_framework import serializers
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    """
    ChatRoom 모델에 대한 시리얼라이저입니다.
    """

    class Meta:
        model = ChatRoom
        fields = ["id", "name", "users", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    """
    Message 모델에 대한 시리얼라이저입니다.
    """

    class Meta:
        model = Message
        fields = ["id", "room", "sender", "content", "timestamp"]
