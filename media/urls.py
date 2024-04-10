from rest_framework import routers
from .views import MediaFileViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('files', MediaFileViewSet)

urlpatterns = router.urls

media_file_predict = MediaFileViewSet.as_view({
    'post': 'predict'
})


urlpatterns = [
    # ...
    path('media/', include('media.urls')),
    path('media/files/<int:pk>/predict/', media_file_predict, name='media-file-predict')
    # ...
]