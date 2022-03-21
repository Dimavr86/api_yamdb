from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin
                    or request.user.is_superuser is True)
        return False


class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
