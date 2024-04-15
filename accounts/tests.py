"""
이 모듈은 Django 테스트 케이스를 정의합니다.
CustomUser 모델과 관련된 테스트가 포함되어 있습니다.
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, UserToken


class CustomUserViewSetTests(APITestCase):
    """
    CustomUser 관련 API 뷰셋에 대한 테스트 케이스입니다.
    """

    def setUp(self):
        """
        테스트 케이스 설정입니다.
        """
        self.superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com",
            password="superpassword",
            nickname="superuser",
        )
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            nickname="admin",
            role="admin",
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword", nickname="testuser"
        )

    def test_create_admin(self):
        """
        관리자 사용자 생성 테스트입니다.
        """
        url = reverse("register-admin")
        data = {
            "email": "newadmin@example.com",
            "password": "newadminpassword",
            "nickname": "newadmin",
            "role": "admin",
        }
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 4)
        self.assertEqual(CustomUser.objects.last().email, "newadmin@example.com")

    def test_register_normal_user(self):
        """
        일반 사용자 등록 테스트입니다.
        """
        token = UserToken.objects.create(user=self.admin).token
        url = reverse("user-register")
        data = {
            "email": "newuser@example.com",
            "password": "newuserpassword",
            "nickname": "newuser",
            "role": "user",
            "token": token,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 4)
        self.assertEqual(CustomUser.objects.last().email, "newuser@example.com")

    def test_login(self):
        """
        사용자 로그인 테스트입니다.
        """
        url = reverse("user-login")
        data = {"email": "testuser@example.com", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_generate_token(self):
        """
        사용자 토큰 생성 테스트입니다.
        """
        url = reverse("user-token-generate", kwargs={"pk": self.superuser.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_delete_user(self):
        """
        사용자 삭제 테스트입니다.
        """
        url = reverse("user-delete", kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_login_check_authenticated(self):
        """
        인증된 사용자 로그인 체크 테스트입니다.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("login-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

    def test_login_check_unauthenticated(self):
        """
        인증되지 않은 사용자 로그인 체크 테스트입니다.
        """
        url = reverse("login-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "failure")
