from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments-list'),
    path('posts/<int:post_pk>/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-comments-detail'),
]