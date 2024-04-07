from rest_framework import serializers
from .models import Tag, Status


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_type', 'tag_content', 'content_type', 'object_id']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'available', 'content_type', 'object_id', 'created_at', 'updated_at']