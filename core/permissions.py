from rest_framework import permissions

from users.models import User
from core.services.page_permission_services import PagePermissionService


class PagePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.is_blocked_forever:
                return request.user.role == User.Roles.ADMIN
            if obj.is_private:
                return any((
                    obj.followers.filter(id=request.user.id).exists(),
                    request.user.role in (User.Roles.ADMIN, User.Roles.MODERATOR),
                    PagePermissionService.user_is_page_owner(request, obj)
                ))
            return True

        if request.method == 'PATCH':
            return PagePermissionService.check_page_patch_permission(request, obj)


class PostPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ('PATCH', 'PUT'):
            return request.user == obj.page.owner
        if request.method == 'DELETE':
            return request.user == obj.page.owner or request.user.role in (User.Roles.ADMIN, User.Roles.MODERATOR)
