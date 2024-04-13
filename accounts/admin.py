# accounts/admin.py
import secrets
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserToken
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserInline(admin.StackedInline):
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
    list_display = ["token", "user", "is_used"]
    fields = ["token", "user", "is_used"]
    readonly_fields = ["token", "user"]

    def save_model(self, request, obj, form, change):
        if not change:
            # 새로운 토큰 생성 시 토큰 값 생성
            obj.token = secrets.token_urlsafe(16)
        super().save_model(request, obj, form, change)


class CustomUserAdmin(UserAdmin):
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
