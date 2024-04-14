from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlarmViewSet, RiskViewSet, AlarmTypeViewSet

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
