from rest_framework import serializers
from .models import Alarm, Risk, AlarmType
from utils.serializers import TagSerializer, StatusSerializer


class RiskSerializer(serializers.ModelSerializer):
    """
    Risk 모델에 대한 serializer.
    Risk 모델 인스턴스를 JSON 등의 포맷으로 직렬화 가능, 직렬화된 데이터에서 Risk 모델 인스턴스를 생성.
    """

    class Meta:
        model = Risk
        fields = ["id", "level", "description"]


class AlarmTypeSerializer(serializers.ModelSerializer):
    """
    AlarmType 모델에 대한 serializer.
    AlarmType 모델 인스턴스를 JSON 등의 포맷으로 직렬화 가능, 직렬화된 데이터에서 AlarmType 모델 인스턴스를 생성 가능.

    Methods
        validate_code(value): 'code' 필드의 유효성을 검사하는 메서드.
        validate_name(value): 'name' 필드의 유효성을 검사하는 메서드.
    """

    class Meta:
        model = AlarmType
        fields = ["id", "code", "name"]

    def validate_code(self, value):
        """
        'code' 필드의 유효성을 검사하는 메서드.

        Parameters
            value (str): 검사할 코드 값.

        Returns
            str: 유효한 코드 값.

        Raises
            ValidationError: 코드 값이 유효하지 않은 경우 발생.
                             코드 값의 길이가 2자를 초과하거나 이미 존재하는 코드인 경우 발생.
        """
        if len(value) > 2:
            raise serializers.ValidationError("code는 2자 이하여야 합니다.")
        if AlarmType.objects.filter(code=value).exists():
            raise serializers.ValidationError("이미 존재하는 code입니다.")
        return value

    def validate_name(self, value):
        """
        'name' 필드의 유효성을 검사하는 메서드.
        이 메서드는 입력된 이름 값의 길이가 20자를 초과하는 경우 ValidationError를 발생.

        Parameters
            value (str): 검사할 이름 값.

        Returns
            str: 유효한 이름 값.

        Raises
            ValidationError: 이름 값이 유효하지 않은 경우 발생.
                             이름 값의 길이가 20자를 초과하는 경우 발생.
        """
        if len(value) > 20:
            raise serializers.ValidationError("name은 20자 이하여야 합니다.")
        return value


class AlarmSerializer(serializers.ModelSerializer):
    """
    Alarm 모델에 대한 serializer.
    Alarm 모델 인스턴스를 JSON 등의 포맷으로 직렬화 가능, 직렬화된 데이터에서 Alarm 모델 인스턴스를 생성 가능.

    Attributes
        tags (TagSerializer): Alarm 모델과 연결된 Tag 모델을 직렬화하는 TagSerializer 필드.
        status (StatusSerializer): Alarm 모델과 연결된 Status 모델을 직렬화하는 StatusSerializer 필드.
        log_format (serializers.ReadOnlyField): 'to_log_format' 메서드의 결과를 직렬화하는 읽기 전용 필드.
    """

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
