from rest_framework import routers
from .views import NoticeViewSet

router = routers.DefaultRouter()
router.register("", NoticeViewSet)

urlpatterns = router.urls
