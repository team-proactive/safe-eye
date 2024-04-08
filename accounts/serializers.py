from rest_framework import serializers
from .models import CustomUser, Status


class CustomUserSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        default=lambda: Status.objects.get(name="Default"),
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "profile_picture",
            "profile_status",
            "profile_message",
            "status",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
