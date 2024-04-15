from django.db import models
from django.conf import settings
from utils.models import TagMixin, StatusMixin


class AlarmType(models.Model):
    """
    알람 유형을 나타내는 모델.
    이 모델은 알람의 유형을 정의, 알람 유형은 Alarm 모델과 외래 키로 연결.

    Attributes
        code (CharField): 알람 유형의 고유한 코드를 저장하는 문자열 필드.
        name (CharField): 알람 유형의 이름을 저장하는 문자열 필드.

    Methods:
        __str__(): 알람 유형의 문자열 표현을 반환하는 메서드.
    """

    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        """
        알람 유형의 문자열 표현을 반환하는 메서드.

        이 메서드는 알람 유형 객체를 문자열로 표현할 때 호출.
        알람 유형의 이름을 리턴.

        Returns
            str: 알람 유형의 이름.
        """
        return self.name


class Risk(models.Model):
    """
    위험 수준을 나타내는 모델.

    이 모델은 알람의 위험 수준을 정의, 위험 수준은 Alarm 모델과 외래 키로 연결.

    Attributes
        RISK_LEVELS (tuple): 위험 수준 선택 옵션을 정의하는 튜플.
        level (CharField): 위험 수준의 코드를 저장하는 문자열 필드.
        description (TextField): 위험에 대한 상세 설명을 저장하는 텍스트 필드.

    Methods:
        __str__(): 위험 수준의 문자열 표현을 반환하는 메서드.
    """

    RISK_LEVELS = (
        ("VL", "매우 낮음"),
        ("LO", "낮음"),
        ("ME", "보통"),
        ("HI", "높음"),
        ("VH", "매우 높음"),
    )

    level = models.CharField(max_length=2, choices=RISK_LEVELS)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        위험 수준의 문자열 표현을 반환하는 메서드.

        이 메서드는 위험 수준 객체를 문자열로 표현할 때 호출.
        위험 수준의 표시 이름을 리턴.

        Returns:
            str: 위험 수준의 표시 이름.
        """
        return self.get_level_display()


class Alarm(TagMixin, StatusMixin, models.Model):
    """
    알람을 나타내는 모델.

    Attributes
        id (AutoField): 알람의 고유 식별자를 자동으로 생성하는 필드.
        admin (ForeignKey): 알람을 생성한 관리자 사용자를 나타내는 외래 키 필드.
        camera_id (IntegerField): 알람이 발생한 카메라의 ID를 저장하는 정수 필드.
        alarm_type (ForeignKey): 알람의 유형을 나타내는 외래 키 필드.
        alarm_content (TextField): 알람의 내용을 저장하는 텍스트 필드.
        risk (ForeignKey): 알람의 위험 수준을 나타내는 외래 키 필드.
        custom_message (TextField): 사용자 정의 메시지를 저장하는 텍스트 필드.
        created_at (DateTimeField): 알람이 생성된 시간을 저장하는 날짜시간 필드.
        updated_at (DateTimeField): 알람이 업데이트된 시간을 저장하는 날짜시간 필드.

    Methods
        __str__(): 알람의 문자열 표현을 반환하는 메서드.
        to_log_format(): 알람을 로그 형식의 문자열로 변환하는 메서드.
    """

    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alarms"
    )
    camera_id = models.IntegerField(default=1)
    alarm_type = models.ForeignKey(AlarmType, on_delete=models.CASCADE)
    alarm_content = models.TextField()
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, default=1)
    custom_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        알람의 문자열 표현을 반환하는 메서드.
        알람 객체를 문자열로 표현할 때 호출. 알람의 유형과 내용을 포함한 문자열을 리턴.
        내용이 길 경우 첫 20자까지만 표시하고 '...'을 붙입니다.

        Returns
            str: 알람의 유형과 내용을 포함한 문자열.
        """
        return f"{self.alarm_type.name} - {self.alarm_content[:20]}..."

    def to_log_format(self):
        """
        알람을 로그 형식의 문자열로 변환하는 메서드.
        알람을 로그로 기록할 때 사용될 수 있는 형식의 문자열을 생성.
        알람의 유형, 카메라 정보, 사용자 정의 메시지, 생성 시간, 위험 수준 등을 포함한 문자열을 리턴.

        Returns:
            str: 알람의 로그 형식 문자열.
        """
        camera_info = f"{self.camera_id}번카메라 에서 " if self.camera_id else ""
        return f"[{self.alarm_type.name}] {camera_info}[{self.custom_message}] {self.created_at.strftime('%Y %m %d %H시 %M분')} [{self.risk.get_level_display()}]"
