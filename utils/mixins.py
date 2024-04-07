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

# 사용자가 객체의 작성자 인지 확인
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
#        return obj.content_object.author == request.user