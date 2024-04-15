from rest_framework import serializers
from .models import Tag, Status


class TagSerializer(serializers.ModelSerializer):
    """
    Tag 모델에 대한 serializer.
    Tag 모델 인스턴스를 JSON 등의 포맷으로 직렬화 가능, 직렬화된 데이터에서 Tag 모델 인스턴스를 생성 가능.
    """

    class Meta:
        model = Tag  # 직렬화에 사용될 모델 클래스를 지정
        fields = [
            "id",
            "tag_type",
            "tag_content",
            "content_type",
            "object_id",
        ]  # 직렬화에 포함될 필드들을 리스트 형태로 지정


class StatusSerializer(serializers.ModelSerializer):
    """
    Status 모델에 대한 serializer입니다.
    Status 모델 인스턴스를 JSON 등의 포맷으로 직렬화 가능, 직렬화된 데이터에서 Status 모델 인스턴스를 생성 가능.
    """

    class Meta:
        model = Status  # 직렬화에 사용될 모델 클래스를 지정
        fields = [
            "id",
            "available",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        ]  # 직렬화에 포함될 필드들을 리스트 형태로 지정
