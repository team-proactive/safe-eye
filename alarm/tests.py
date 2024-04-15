from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Alarm, AlarmType, Risk
from accounts.models import CustomUser


class AlarmViewSetTestCase(APITestCase):
    """
    AlarmViewSet에 대한 테스트 케이스.

    Methods
        setUp(): 테스트에 필요한 초기 설정을 수행.
        test_create_alarm(): 알람 생성 기능을 테스트.
        test_list_alarms(): 알람 목록 조회 기능을 테스트.
        test_receive_alarm_data(): 알람 데이터 수신 기능을 테스트.
        test_update_alarm(): 알람 업데이트 기능을 테스트.
    """

    def setUp(self):
        """
        테스트에 필요한 초기 설정을 수행.

        - APIClient를 생성, 관리자 사용자를 생성, 알람 유형과 위험 수준 객체를 생성.
        """
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
        """
        알람 생성 기능을 테스트.

        - 알람 생성 API 엔드포인트의 URL을 가져오고, 알람 생성에 필요한 데이터를 준비.
        - 관리자 사용자로 인증하고, 알람 생성 API 엔드포인트에 POST 요청을 보냄.
        - 응답 상태 코드가 201 (Created)인지 확인하고, 생성된 알람의 개수가 1개인지 확인.
        """
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
        """
        알람 목록 조회 기능을 테스트.

        - 알람 목록 조회 API 엔드포인트의 URL을 가져오고, 테스트용 알람을 생성.
        - 알람 목록 조회 API 엔드포인트에 GET 요청을 보내고, 응답 상태 코드가 200 (OK)인지 확인.
        - 응답으로 받은 알람 목록의 개수가 1개인지 확인.
        """
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
        """
        알람 데이터 수신 기능을 테스트.

        - 알람 데이터 수신 API 엔드포인트의 URL을 가져오고, 수신할 알람 데이터를 준비.
        - 관리자 사용자로 인증하고, 알람 데이터 수신 API 엔드포인트에 POST 요청을 보냄. 요청에는 알람 데이터를 JSON 형식으로 포함.
        - 응답 상태 코드가 200 (OK)인지 확인하고, 수신된 알람 데이터로 생성된 알람의 개수가 1개인지 확인.
        """
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
        """
        알람 업데이트 기능을 테스트.

        - 테스트용 알람을 생성하고, 알람 업데이트 API 엔드포인트의 URL을 가져옴.
        - 업데이트할 알람 데이터를 준비하고, 관리자 사용자로 인증.
        - 알람 업데이트 API 엔드포인트에 PUT 요청을 보내고, 응답 상태 코드가 200 (OK)인지 확인.
        - 업데이트된 알람의 정보 확인.(카메라 ID가 변경되었는지 확인하고, 알람 내용이 변경되었는지 확인.)
        """
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
