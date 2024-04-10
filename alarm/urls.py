from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlarmViewSet

router = DefaultRouter()
router.register(r"alarms", AlarmViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
