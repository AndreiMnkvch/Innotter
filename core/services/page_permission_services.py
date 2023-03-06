from rest_framework.request import Request
from core.models import Page
from users.models import User


class PagePermissionService:
    ADMIN_CAN_CHANGE_FIELDS = {'unblock_date', 'is_blocked_forever'}
    MODERATOR_CAN_CHANGE_FIELDS = {'unblock_date'}
    USER_CAN_CHANGE_FIELDS = {
        'name', 'description', 'is_private', 'tags', 'image'}

    @staticmethod
    def check_fields_are_allowed(request: Request, allowed_fields: set[str]) -> bool:
        return set(request.data).issubset(allowed_fields)

    @staticmethod
    def user_is_page_owner(request: Request, obj: Page) -> bool:
        return request.user == obj.owner

    @staticmethod
    def check_page_patch_permission(request: Request, obj: Page) -> bool:
        """ forbids updating page's not allowed fields in request.data for corresponding user type """

        if request.user.role == User.Roles.ADMIN:
            return PagePermissionService.check_fields_are_allowed(request, PagePermissionService.ADMIN_CAN_CHANGE_FIELDS)
        elif request.user.role == User.Roles.MODERATOR:
            return PagePermissionService.check_fields_are_allowed(request, PagePermissionService.MODERATOR_CAN_CHANGE_FIELDS)
        elif request.user.role == User.Roles.USER:
            return all((
                PagePermissionService.check_fields_are_allowed(
                    request, PagePermissionService.USER_CAN_CHANGE_FIELDS),
                PagePermissionService.user_is_page_owner(request, obj)
            ))

    @staticmethod
    def check_page_post_permission(request: Request) -> bool:
        """ forbids creating new page with not allowed fields in request.data for corresponding user type """

        if request.user.role == User.Roles.ADMIN:
            return PagePermissionService.check_fields_are_allowed(request, PagePermissionService.ADMIN_CAN_CHANGE_FIELDS)
        if request.user.role == User.Roles.MODERATOR:
            return PagePermissionService.check_fields_are_allowed(request, PagePermissionService.MODERATOR_CAN_CHANGE_FIELDS)
        if request.user.role == User.Roles.USER:
            return PagePermissionService.check_fields_are_allowed(request, PagePermissionService.USER_CAN_CHANGE_FIELDS)
