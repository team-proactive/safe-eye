from rest_framework import serializers
from .models import Tag, Status


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "tag_type", "tag_content", "content_type", "object_id"]
        extra_kwargs = {
            "tag_type": {"required": False},
            "tag_content": {"required": False},
            "content_type": {"required": False},
            "object_id": {"required": False},
        }


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            "id",
            "available",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "available": {"required": False},
            "content_type": {"required": False},
            "object_id": {"required": False},
        }
