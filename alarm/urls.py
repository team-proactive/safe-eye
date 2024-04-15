from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlarmViewSet, RiskViewSet, AlarmTypeViewSet

"""
alarm 앱의 URL 설정 모듈.
alarm 앱의 URL 패턴을 정의.
"""

router = DefaultRouter()
router.register(r"alarms", AlarmViewSet)
router.register(r"risks", RiskViewSet)
router.register(r"alarm-types", AlarmTypeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "receive-alarm-data/",
        AlarmViewSet.as_view({"post": "receive_alarm_data"}),
        name="receive-alarm-data",
    ),
]
