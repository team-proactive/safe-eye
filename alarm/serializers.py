from rest_framework import serializers
from .models import Alarm, Risk, AlarmType
from utils.serializers import TagSerializer, StatusSerializer


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ["id", "level", "description"]


class AlarmTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmType
        fields = ["id", "code", "name"]

    def validate_code(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("code는 2자 이하여야 합니다.")
        if AlarmType.objects.filter(code=value).exists():
            raise serializers.ValidationError("이미 존재하는 code입니다.")
        return value

    def validate_name(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("name은 20자 이하여야 합니다.")
        return value


class AlarmSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    status = StatusSerializer(many=True, required=False)
    log_format = serializers.ReadOnlyField(source="to_log_format")

    class Meta:
        model = Alarm
        fields = [
            "id",
            "admin",
            "camera_id",
            "alarm_type",
            "alarm_content",
            "risk",
            "custom_message",
            "created_at",
            "updated_at",
            "tags",
            "status",
            "log_format",
        ]
