# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from utils.models import Status
from .models import UserToken
import logging

logger = logging.getLogger(__name__)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            role=validated_data["role"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, data):
        logger.debug("Received authentication data: %s", data)
        user = authenticate(**data)
        if user and user.is_active:
            logger.debug("Authentication successful for user: %s", user)
            return {"user": user}
        else:
            logger.warning("Authentication failed for data: %s", data)
            # Here, we log more details why authenticate could have failed
            try:
                user_obj = get_user_model().objects.get(email=data.get("email"))
                if user_obj.check_password(data.get("password")):
                    logger.debug(
                        "Password is correct, so the issue may be with the authentication backend."
                    )
                else:
                    logger.debug("Password is incorrect.")
            except get_user_model().DoesNotExist:
                logger.debug("No user found with this email address.")
            raise serializers.ValidationError(
                "Unable to login with provided credentials."
            )


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "nickname", "role"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)  # 클라이언트로부터 토큰을 받기 위해

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_token(self, value):
        # 토큰 검증
        if not UserToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid token")
        return value

    def create(self, validated_data):
        token = validated_data.pop("token")
        user_token = UserToken.objects.get(
            token=token
        )  # 토큰으로부터 어드민 유저 가져오기
        user = get_user_model().objects.create_user(
            admin=user_token.user,
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            role=validated_data["role"],
        )
        user_token.delete()  # 사용된 토큰은 삭제
        return user


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = ["token"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)  # 클라이언트로부터 토큰을 받기 위해

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_token(self, value):
        # 토큰 검증
        if not UserToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid token")
        return value

    def create(self, validated_data):
        token = validated_data.pop("token")
        user_token = UserToken.objects.get(
            token=token
        )  # 토큰으로부터 어드민 유저 가져오기
        user = get_user_model().objects.create_user(
            admin=user_token.user,
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            role=validated_data["role"],
        )
        user_token.delete()  # 사용된 토큰은 삭제
        return user
