from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Status


class CustomUserTests(APITestCase):
    def setUp(self):
        self.default_status = Status.objects.create(name="Default")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "status": self.default_status.id,
            # 필요한 다른 사용자 필드들 추가
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_signup(self):
        url = reverse("customuser-list")
        data = {
            "username": "newuser",
            "password": "newpassword",
            # 필요한 다른 사용자 필드들 추가
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.last().status.name, "Default")

    # 다른 테스트 케이스들 추가
