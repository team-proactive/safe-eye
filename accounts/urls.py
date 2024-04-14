from django.urls import path
from .views import CustomUserViewSet, UserRegistrationViewSet

urlpatterns = [
    path("login/", CustomUserViewSet.as_view({"post": "login"}), name="user-login"),
    path("logout/", CustomUserViewSet.as_view({"post": "logout"}), name="user-logout"),
    path(
        "register-admin/",
        CustomUserViewSet.as_view({"post": "create"}),
        name="register-admin",
    ),
    path(
        "register/",
        UserRegistrationViewSet.as_view({"post": "register"}),
        name="user-register",
    ),
    path("users/", CustomUserViewSet.as_view({"get": "list"}), name="user-list"),
    path(
        "<int:pk>/",
        CustomUserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="user-detail",
    ),
    path(
        "<int:pk>/delete/",
        CustomUserViewSet.as_view({"delete": "delete_user"}),
        name="user-delete",
    ),
    path(
        "<int:pk>/tokens/generate/",
        CustomUserViewSet.as_view({"post": "generate_token"}),
        name="user-token-generate",
    ),
    path(
        "<int:pk>/tokens/generate/",
        CustomUserViewSet.as_view({"post": "generate_token"}),
        name="user-token-generate",
    ),
]
