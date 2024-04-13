from rest_framework import serializers
from .models import Alarm, Risk, AlarmType
from utils.serializers import TagSerializer, StatusSerializer
from utils.models import Tag, Status


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ["id", "level", "description"]


class AlarmTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlarmType
        fields = ["id", "code", "name"]


class AlarmSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    status = StatusSerializer(many=True, required=False)
    alarm_type = AlarmTypeSerializer()
    risk = RiskSerializer()

    class Meta:
        model = Alarm
        fields = [
            "id",
            "user",
            "camera_id",
            "alarm_type",
            "alarm_content",
            "risk",
            "custom_message",
            "created_at",
            "updated_at",
            "tags",
            "status",
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        status_data = validated_data.pop("status", [])
        alarm = Alarm.objects.create(**validated_data)

        for tag_data in tags_data:
            Tag.objects.create(content_object=alarm, **tag_data)
        for status_data_item in status_data:
            Status.objects.create(content_object=alarm, **status_data_item)

        return alarm

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        status_data = validated_data.pop("status", [])

        instance = super().update(instance, validated_data)

        instance.tags.all().delete()
        instance.status.all().delete()

        for tag_data in tags_data:
            Tag.objects.create(content_object=instance, **tag_data)
        for status_data_item in status_data:
            Status.objects.create(content_object=instance, **status_data_item)

        return instance

    def validate(self, data):
        # 필수 필드 유효성 검사
        if "alarm_type" not in data:
            raise serializers.ValidationError("alarm_type is required.")
        if "alarm_content" not in data:
            raise serializers.ValidationError("alarm_content is required.")
        if "risk" not in data:
            raise serializers.ValidationError("risk is required.")
        if "user" not in data:
            raise serializers.ValidationError("user is required.")
        return data
