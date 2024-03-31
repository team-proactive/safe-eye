from rest_framework import routers
from .views import NoticeViewSet

router = routers.DefaultRouter()
router.register("notices", NoticeViewSet)

urlpatterns = router.urls
