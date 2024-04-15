"""
Chat 앱의 모델을 정의하는 모듈입니다.
ChatRoom과 Message 모델을 포함하고 있습니다.
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    """
    채팅방을 나타내는 모델입니다.
    """

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="chat_rooms")
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """
    채팅 메시지를 나타내는 모델입니다.
    """

    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
