from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj):

        return obj.username == request.user


class MyUserPermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, obj):

        if request.user.is_authenticated and request.user.is_superuser:
            return True

        if isinstance(obj, User):
            return obj == request.user

        return False
