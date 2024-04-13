# accounts/views.py
import logging
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


logger = logging.getLogger(__name__)


class UserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User Registration with Token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, example="test@example.com"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, example="test123123!@#"
                ),
                "nickname": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
                "token": openapi.Schema(type=openapi.TYPE_STRING, example="abc123"),
            },
            required=["email", "password", "nickname", "token"],
        ),
        responses={201: openapi.Response("User successfully registered.")},
    )
    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        user_token = UserToken.objects.filter(token=token, is_used=False).first()
        if not user_token:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 토큰 사용 처리
        user_token.user = user
        user_token.is_used = True
        user_token.save()

        return Response(
            {
                "user": CustomUserSerializer(user).data,
                "message": "User successfully registered.",
            },
            status=status.HTTP_201_CREATED,
        )


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "login":
            return UserLoginSerializer

        elif self.action == "generate_token":
            return UserTokenSerializer
        return CustomUserSerializer

    def get_permissions(self):
        if self.action in ["generate_token", "delete_user"]:
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

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def refresh(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
