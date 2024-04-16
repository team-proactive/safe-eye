# accounts/permissions.py

"""
이 모듈은 Django REST Framework 권한 클래스를 정의합니다.
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    관리자 사용자 권한을 확인하는 권한 클래스입니다.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
