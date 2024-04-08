from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, StatusViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet)
router.register(r"status", StatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
