from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, StatusViewSet

router = DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"status", StatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
