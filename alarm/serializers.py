from rest_framework import serializers
from .models import Alarm
from utils.serializers import TagSerializer, StatusSerializer
from utils.models import Tag, Status


class AlarmSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    status = StatusSerializer(many=True, required=False)

    class Meta:
        model = Alarm
        fields = [
            "id",
            "user",
            "alarm_type",
            "alarm_content",
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
