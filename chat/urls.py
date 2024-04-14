from django.urls import path
from . import views

urlpatterns = [
    path("rooms/", views.ChatRoomList.as_view(), name="room_list"),
    path(
        "rooms/<int:room_id>/messages/",
        views.MessageList.as_view(),
        name="message_list",
    ),
]
