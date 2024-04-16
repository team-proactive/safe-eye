from django.test import TestCase, RequestFactory
from django.http import Http404
from django.views import View
from .mixins import Custom404Mixin, IsAuthorOrReadOnly
from accounts.models import CustomUser
from alarm.models import Alarm, AlarmType, Risk


class TestView(Custom404Mixin, View):
    """
    Custom404Mixin을 테스트하기 위한 뷰.
    """

    custom_404_message = "Custom 404 message"

    def get(self, request):
        """
        GET 요청을 처리하고 Http404 예외를 발생.

        Parameters:
        request (HttpRequest): HTTP 요청 객체.

        Raises:
        Http404: 페이지를 찾을 수 없음을 나타내는 예외.
        """
        raise Http404()


class Custom404MixinTestCase(TestCase):
    """
    Custom404Mixin에 대한 테스트 케이스.
    """

    def setUp(self):
        """
        테스트에 필요한 설정을 수행.
        """
        self.factory = RequestFactory()
        self.view = TestView.as_view()

    def test_dispatch_with_http404(self):
        """
        Custom404Mixin의 dispatch 메서드를 테스트.
        """
        request = self.factory.get("/non-existent-url/")
        response = self.view(request)
        self.assertEqual(response.status_code, 404)


class IsAuthorOrReadOnlyTestCase(TestCase):
    """
    IsAuthorOrReadOnly 권한 클래스에 대한 테스트 케이스.
    """

    def setUp(self):
        """
        테스트에 필요한 설정을 수행.
        """
        self.factory = RequestFactory()
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="adminpassword",
            role="admin",
            nickname="admin",
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword", nickname="testuser"
        )

        self.alarm_type = AlarmType.objects.create(code="FI", name="Fire")
        self.risk = Risk.objects.create(level="HI", description="High Risk")
        self.alarm = Alarm.objects.create(
            admin=self.admin,
            camera_id=1,
            alarm_type=self.alarm_type,
            alarm_content="Test Alarm",
            risk=self.risk,
        )
        self.permission = IsAuthorOrReadOnly()

    def test_has_object_permission_safe_methods(self):
        """
        안전한 메서드에 대한 객체 권한을 테스트.
        """
        request = self.factory.get("/")
        request.user = self.user
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertTrue(result)

    def test_has_object_permission_author(self):
        """
        작성자의 객체 권한을 테스트.
        """
        request = self.factory.post("/")
        request.user = self.admin
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertTrue(result)

    def test_has_object_permission_non_author(self):
        """
        작성자가 아닌 사용자의 객체 권한을 테스트.
        """
        request = self.factory.post("/")
        request.user = self.user
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertFalse(result)
