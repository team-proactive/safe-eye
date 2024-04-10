from django.test import TestCase

# Create your tests here.
# alarms/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Alarm

User = get_user_model()


class AlarmTests(APITestCase):
    def setUp(self):
        print("테스트 준비 중...")
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            nickname="testuser",
        )
        self.superuser = User.objects.create_superuser(
            email="superuser@example.com",
            password="superpassword",
            nickname="superuser",
        )
        self.alarm = Alarm.objects.create(
            alarm_type="FD",
            alarm_content="Test Alarm",
        )
        self.alarm_data = {
            "alarm_type": "BR",
            "alarm_content": "New Alarm",
        }
        print("테스트 준비 완료")

    def test_alarm_list(self):
        print("알람 목록 조회 테스트 시작")
        url = reverse("alarm-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("알람 목록 조회 테스트 완료")

    def test_alarm_create_by_superuser(self):
        print("Superuser의 알람 생성 테스트 시작")
        url = reverse("alarm-list")
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, self.alarm_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.superuser.id)
        print("Superuser의 알람 생성 테스트 완료")

    def test_alarm_create_by_user(self):
        print("일반 사용자의 알람 생성 테스트 시작")
        url = reverse("alarm-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.alarm_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["user"])
        print("일반 사용자의 알람 생성 테스트 완료")

    def test_alarm_retrieve(self):
        print("알람 조회 테스트 시작")
        url = reverse("alarm-detail", args=[self.alarm.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("알람 조회 테스트 완료")

    def test_alarm_update_by_superuser(self):
        print("Superuser의 알람 수정 테스트 시작")
        url = reverse("alarm-detail", args=[self.alarm.id])
        self.client.force_authenticate(user=self.superuser)
        response = self.client.put(url, self.alarm_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.superuser.id)
        print("Superuser의 알람 수정 테스트 완료")

    def test_alarm_update_by_user(self):
        print("일반 사용자의 알람 수정 테스트 시작")
        url = reverse("alarm-detail", args=[self.alarm.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, self.alarm_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("일반 사용자의 알람 수정 테스트 완료")

    def test_alarm_delete_by_superuser(self):
        print("Superuser의 알람 삭제 테스트 시작")
        url = reverse("alarm-detail", args=[self.alarm.id])
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        print("Superuser의 알람 삭제 테스트 완료")

    def test_alarm_delete_by_user(self):
        print("일반 사용자의 알람 삭제 테스트 시작")
        url = reverse("alarm-detail", args=[self.alarm.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("일반 사용자의 알람 삭제 테스트 완료")
