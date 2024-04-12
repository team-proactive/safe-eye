# accounts/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, UserToken
from .serializers import (
    CustomUserSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    UserTokenSerializer,
    UserRegistrationSerializer,
)
from .permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "login":
            return UserLoginSerializer
        elif self.action == "register_normal_user":
            return UserRegistrationSerializer
        elif self.action == "generate_token":
            return UserTokenSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action in ["login", "register_normal_user", "list"]:
            return [AllowAny()]
        elif self.action in ["generate_token", "delete_user"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        method="post",
        operation_description="User Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, example="test@example.com"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, example="test123123!@#"
                ),
            },
            required=["email", "password"],
        ),
        responses={200: UserLoginSerializer()},
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": CustomUserSerializer(user).data,
            }
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="register-normal-user",
        url_name="register-normal-user",
        permission_classes=[AllowAny],
    )
    def register_normal_user(self, request):
        """Register a normal user with a token validation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": CustomUserSerializer(user).data,
                "message": "User successfully registered.",
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="generate-token",
        url_name="generate-token",
    )
    def generate_token(self, request, pk=None):
        """Generate a registration token for a user."""
        user = self.get_object()
        if user.role != "superuser":
            return Response(
                {"detail": "Only superusers can generate tokens."},
                status=status.HTTP_403_FORBIDDEN,
            )
        token = UserToken.objects.create(user=user)
        return Response({"token": token.token}, status=status.HTTP_201_CREATED)

    @action(
        detail=True, methods=["delete"], url_path="delete-user", url_name="delete-user"
    )
    def delete_user(self, request, pk=None):
        """Delete a user account."""
        user = self.get_object()
        if request.user.role != "superuser" and request.user != user:
            return Response(
                {"detail": "You don't have permission to delete this user."},
                status=status.HTTP_403_FORBIDDEN,
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
