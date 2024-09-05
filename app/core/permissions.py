from rest_framework import permissions

from accounts.enums import UserRole


def is_admin_only(request):
    if not request.user.is_authenticated:
        return False

    if request.user.type == UserRole.ADMIN:
        return True


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_admin_only(request):
            return True
        return False
