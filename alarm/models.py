from django.db import models
from django.conf import settings
from utils.models import TagMixin, StatusMixin


class Alarm(TagMixin, StatusMixin, models.Model):
    ALARM_TYPES = (
        ("FD", "전도"),
        ("BR", "파손"),
        ("AR", "방화"),
        ("SM", "흡연"),
        ("AB", "유기"),
        ("TH", "절도"),
        ("AS", "폭행"),
        ("TV", "교통약자"),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    alarm_type = models.CharField(max_length=2, choices=ALARM_TYPES)
    alarm_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_alarm_type_display()} - {self.alarm_content[:20]}..."
