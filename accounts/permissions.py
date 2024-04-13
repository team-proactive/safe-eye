# accounts/permissions.py

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
