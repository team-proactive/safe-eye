from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions


class Custom404Mixin:
    custom_404_message = None

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            message = self.custom_404_message or "페이지를 찾을 수 없습니다."
            context = {"message": message}
            return render(request, "custom_404.html", context, status=404)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 객체에 user 필드가 없는 경우
        if not hasattr(obj, "user"):
            # 수퍼유저에게만 쓰기 권한 부여
            return request.user.is_superuser

        # 객체에 user 필드가 있는 경우
        if hasattr(obj, "user"):
            # 객체의 소유자이거나 수퍼유저인 경우에만 쓰기 권한 부여
            return obj.user == request.user or request.user.is_superuser

        # 그 외의 경우 쓰기 권한 거부
        return False
