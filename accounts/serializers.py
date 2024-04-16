# accounts/serializers.py

"""
이 모듈은 Django REST Framework 시리얼라이저를 정의합니다.
CustomUser 모델과 관련된 시리얼라이저가 포함되어 있습니다.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from utils.models import Status
from .models import UserToken
import logging

logger = logging.getLogger(__name__)


class UserCreateSerializer(serializers.ModelSerializer):
    """
    새로운 사용자를 생성하기 위한 시리얼라이저입니다.
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        검증된 데이터를 사용하여 새로운 CustomUser 인스턴스를 생성합니다.
        """

        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
            role=validated_data["role"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    사용자 로그인을 위한 시리얼라이저입니다.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, data):
        """
        제공된 인증 데이터를 검증합니다.
        """

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
    """
    CustomUser 모델에 대한 일반적인 시리얼라이저입니다.
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "nickname", "role"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    새로운 사용자 등록을 위한 시리얼라이저입니다.
    """

    token = serializers.CharField(write_only=True)  # 클라이언트로부터 토큰을 받기 위해

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_token(self, value):
        """
        제공된 토큰의 유효성을 검증합니다.
        """
        # 토큰 검증
        if not UserToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid token")
        return value

    def create(self, validated_data):
        """
        검증된 데이터를 사용하여 새로운 CustomUser 인스턴스를 생성합니다.
        """

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
    """
    UserToken 모델에 대한 시리얼라이저입니다.
    """

    class Meta:
        model = UserToken
        fields = ["token"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    새로운 사용자 등록을 위한 시리얼라이저입니다.
    """

    token = serializers.CharField(write_only=True)  # 클라이언트로부터 토큰을 받기 위해

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "nickname", "role", "token"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_token(self, value):
        """
        제공된 토큰의 유효성을 검증합니다.
        """

        # 토큰 검증
        if not UserToken.objects.filter(token=value).exists():
            raise serializers.ValidationError("Invalid token")
        return value

    def create(self, validated_data):
        """
        검증된 데이터를 사용하여 새로운 CustomUser 인스턴스를 생성합니다.
        """

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
