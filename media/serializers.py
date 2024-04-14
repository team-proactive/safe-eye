from rest_framework import serializers
from .models import MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'created_at', 'description', 'file_size', 'file_type', 'ai_model', 'result']