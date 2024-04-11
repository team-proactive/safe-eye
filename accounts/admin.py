from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "is_staff",
        "is_superuser",
    )  # 'username' 대신 실제 필드 이름 사용
    ordering = ("email",)  # 'username' 대신 실제 필드 이름 사용


admin.site.register(CustomUser, CustomUserAdmin)
