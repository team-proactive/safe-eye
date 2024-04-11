# accounts > tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser


class CustomUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "nickname": "Test User",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """
        사용자 생성 테스트
        """
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.nickname, self.user_data["nickname"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))

    def test_user_login(self):
        """
        사용자 로그인 테스트
        """
        url = reverse("customuser-login")
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_user_update(self):
        """
        사용자 정보 수정 테스트
        """
        url = reverse("customuser-detail", args=[self.user.id])
        updated_data = {
            "nickname": "Updated User",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, updated_data["nickname"])

    def test_user_delete(self):
        """
        사용자 삭제 테스트
        """
        url = reverse("customuser-detail", args=[self.user.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 0)
