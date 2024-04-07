from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', views.TagRetrieveUpdateDestroyAPIView.as_view(), name='tag-retrieve-update-destroy'),
    
    path('status/', views.StatusListCreateAPIView.as_view(), name='status-list-create'),
    path('status/<int:pk>/', views.StatusRetrieveUpdateDestroyAPIView.as_view(), name='status-retrieve-update-destroy'),
]