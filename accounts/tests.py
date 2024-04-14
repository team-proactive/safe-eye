from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser, UserToken


class CustomUserViewSetTests(APITestCase):
    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com", password="superpassword"
        )
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com", password="adminpassword", role="admin"
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_create_admin(self):
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
        url = reverse("user-login")
        data = {"email": "testuser@example.com", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_generate_token(self):
        url = reverse("user-token-generate", kwargs={"pk": self.superuser.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_delete_user(self):
        url = reverse("user-delete", kwargs={"pk": self.user.pk})
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_login_check_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("login-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

    def test_login_check_unauthenticated(self):
        url = reverse("login-check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "failure")
