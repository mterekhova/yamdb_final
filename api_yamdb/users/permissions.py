from rest_framework import permissions


class OwnerOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AdminOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request._user.is_superuser or request._user.role == 'admin'
