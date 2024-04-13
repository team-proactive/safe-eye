from django.db import models
from django.conf import settings
from utils.models import TagMixin, StatusMixin


class AlarmType(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Risk(models.Model):
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
        return self.get_level_display()


class Alarm(TagMixin, StatusMixin, models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
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
        return f"{self.alarm_type.name} - {self.alarm_content[:20]}..."
