from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, StatusViewSet

"""
utils 앱의 URL 설정 모듈.
utils 앱의 URL 패턴을 정의.
"""

router = DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"status", StatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
