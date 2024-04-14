from rest_framework_nested import routers
from .views import ChatRoomViewSet, MessageViewSet

router = routers.SimpleRouter()
router.register(r"rooms", ChatRoomViewSet)

messages_router = routers.NestedSimpleRouter(router, r"rooms", lookup="room")
messages_router.register(r"messages", MessageViewSet, basename="room-messages")

urlpatterns = [
    *router.urls,
    *messages_router.urls,
]
