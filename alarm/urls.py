from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlarmViewSet, RiskViewSet

router = DefaultRouter()
router.register(r"alarms", AlarmViewSet)
router.register(r"risks", RiskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(router.urls)),
]
