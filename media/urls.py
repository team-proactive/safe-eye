from rest_framework import routers
from .views import MediaFileViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('files', MediaFileViewSet)

urlpatterns = router.urls


urlpatterns = [
    # ...
    path('media/', include('media.urls')),
    # ...
]