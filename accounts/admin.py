from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # 필요한 필드만 명시
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "nickname",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Permissions", {"fields": ("user_permissions", "groups")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "nickname",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    list_display = ["email", "nickname", "is_staff", "is_active"]
    search_fields = ("email", "nickname")
    ordering = ("email",)
