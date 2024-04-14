from django.test import TestCase, RequestFactory
from django.http import Http404
from django.views import View
from .mixins import Custom404Mixin, IsAuthorOrReadOnly
from accounts.models import CustomUser
from alarm.models import Alarm, AlarmType, Risk


class TestView(Custom404Mixin, View):
    custom_404_message = "Custom 404 message"

    def get(self, request):
        raise Http404()


class Custom404MixinTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = TestView.as_view()

    def test_dispatch_with_http404(self):
        request = self.factory.get("/non-existent-url/")
        response = self.view(request)
        self.assertEqual(response.status_code, 404)


class IsAuthorOrReadOnlyTestCase(TestCase):
    def setUp(self):
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
        request = self.factory.get("/")
        request.user = self.user
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertTrue(result)

    def test_has_object_permission_author(self):
        request = self.factory.post("/")
        request.user = self.admin
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertTrue(result)

    def test_has_object_permission_non_author(self):
        request = self.factory.post("/")
        request.user = self.user
        result = self.permission.has_object_permission(request, None, self.alarm)
        self.assertFalse(result)
