from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class ChatTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.room = ChatRoom.objects.create(name="Test Room")
        self.room.users.add(self.user1, self.user2)

    def test_create_chat_room(self):
        room_name = "New Room"
        response = self.client.post("/chat/rooms/", {"name": room_name})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ChatRoom.objects.count(), 2)
        self.assertEqual(ChatRoom.objects.last().name, room_name)

    def test_send_message(self):
        message_content = "Test Message"
        response = self.client.post(
            f"/chat/rooms/{self.room.id}/messages/",
            {"sender": self.user1.id, "content": message_content},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().content, message_content)
