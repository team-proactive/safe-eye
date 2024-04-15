from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class ChatRoomTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_create_chat_room(self):
        url = reverse("chatroom-list")
        data = {"name": "Test Room"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 1)
        self.assertEqual(ChatRoom.objects.get().name, "Test Room")

    def test_retrieve_chat_room(self):
        room = ChatRoom.objects.create(name="Test Room")
        url = reverse("chatroom-detail", args=[room.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Room")


class MessageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.chat_room = ChatRoom.objects.create(name="Test Room")

    def test_create_message(self):
        url = reverse("message-list", kwargs={"room_pk": self.chat_room.id})
        data = {"content": "Test Message"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.last().content, "Test Message")

    def test_list_messages(self):
        Message.objects.create(
            room=self.chat_room, sender=self.user, content="Message 1"
        )
        Message.objects.create(
            room=self.chat_room, sender=self.user, content="Message 2"
        )
        url = reverse("message-list", kwargs={"room_pk": self.chat_room.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
