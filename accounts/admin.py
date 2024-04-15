# accounts/admin.py
"""
이 모듈은 Django 관리자 페이지 설정을 정의합니다.
CustomUser 모델과 UserToken 모델에 대한 관리자 인터페이스가 포함되어 있습니다.
"""

import secrets
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserToken
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserInline(admin.StackedInline):
    """
    CustomUser 모델에 대한 인라인 편집기입니다.
    """

    model = CustomUser
    can_delete = False
    verbose_name_plural = "Subordinate Users"
    fields = ["email", "nickname", "role", "password"]
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == "superuser" or request.user.role == "admin":
            return qs
        else:
            return qs.none()


class UserTokenAdmin(admin.ModelAdmin):
    """
    UserToken 모델에 대한 관리자 인터페이스입니다.
    """

    list_display = ["token", "user", "is_used"]
    fields = ["token", "user", "is_used"]
    readonly_fields = ["token", "user"]

    def save_model(self, request, obj, form, change):
        if not change:
            # 새로운 토큰 생성 시 토큰 값 생성
            obj.token = secrets.token_urlsafe(16)
        super().save_model(request, obj, form, change)


class CustomUserAdmin(UserAdmin):
    """
    CustomUser 모델에 대한 관리자 인터페이스입니다.
    """

    model = CustomUser
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
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

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return self.fieldsets
        elif request.user.role == "admin":
            return self.fieldsets
        else:
            # 하위 사용자(User)에게는 일부 필드만 표시
            return ((None, {"fields": ("email", "nickname")}),)

    def get_inlines(self, request, obj=None):
        if request.user.is_superuser:
            return [CustomUserInline]
        elif request.user.role == "admin":
            return [CustomUserInline]
        else:
            return []

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
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
    list_display = ["email", "nickname", "role", "is_staff", "is_active"]
    search_fields = ("email", "nickname")
    ordering = ("email",)
    inlines = [CustomUserInline]

    def save_model(self, request, obj, form, change):
        if not change and obj.role != "superuser":
            # 새로운 사용자 생성 시 토큰 생성
            token = secrets.token_urlsafe(16)
            user_token = UserToken(token=token)
            user_token.save()
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserToken, UserTokenAdmin)
