from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/update/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    path('status/', views.StatusListView.as_view(), name='status_list'),
    path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]