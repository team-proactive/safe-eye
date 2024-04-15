"""
Chat 앱의 뷰를 정의하는 모듈입니다.
ChatRoomViewSet과 MessageViewSet을 포함하고 있습니다.
"""

from rest_framework import viewsets
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    ChatRoom 모델에 대한 ViewSet입니다.
    """

    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    Message 모델에 대한 ViewSet입니다.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs["room_pk"]
        return Message.objects.filter(room_id=room_id)
