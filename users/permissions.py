from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import User


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        #admin to block users
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PATCH':
            return request.user.role == User.Roles.ADMIN
        if request.method == 'DELETE':
            #there is an opportunity to delete user only from django admin site
            return False



