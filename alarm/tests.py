from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Alarm, AlarmType, Risk
from accounts.models import CustomUser


class AlarmViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            role="admin",
            nickname="admin",
        )
        self.alarm_type = AlarmType.objects.create(code="FI", name="화재")
        self.risk = Risk.objects.create(level="HI", description="높음")

    def test_create_alarm(self):
        url = reverse("alarm-list")
        data = {
            "admin": self.admin.id,
            "camera_id": 1,
            "alarm_type": self.alarm_type.id,
            "alarm_content": "화재 발생",
            "risk": self.risk.id,
            "custom_message": "119에 신고 필요",
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alarm.objects.count(), 1)

    def test_list_alarms(self):
        url = reverse("alarm-list")
        Alarm.objects.create(
            admin=self.admin,
            camera_id=1,
            alarm_type=self.alarm_type,
            alarm_content="화재 발생",
            risk=self.risk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_receive_alarm_data(self):
        url = reverse("receive-alarm-data")
        data = {
            "status": "화재 발생",
            "risk_level": "HI",
            "alarm_type_code": "FI",
            "custom_message": "119에 신고 필요",
            "camera_id": 1,
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Alarm.objects.count(), 1)

    def test_update_alarm(self):
        alarm = Alarm.objects.create(
            admin=self.admin,
            camera_id=1,
            alarm_type=self.alarm_type,
            alarm_content="화재 발생",
            risk=self.risk,
        )
        url = reverse("alarm-detail", kwargs={"pk": alarm.pk})
        data = {
            "admin": self.admin.id,
            "camera_id": 2,
            "alarm_type": self.alarm_type.id,
            "alarm_content": "화재 상황 종료",
            "risk": self.risk.id,
            "custom_message": "상황 종료",
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alarm.refresh_from_db()
        self.assertEqual(alarm.camera_id, 2)
        self.assertEqual(alarm.alarm_content, "화재 상황 종료")
