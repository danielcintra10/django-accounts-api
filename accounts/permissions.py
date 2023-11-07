from rest_framework import permissions


class IsAuthenticatedAndIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return request.user.email == obj.email
