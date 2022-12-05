from typing import Tuple

from rest_framework.request import Request

from users.models import User


ADMIN_CAN_CHANGE_FIELDS = ('unblock_date', 'is_blocked_forever')
MODERATOR_CAN_CHANGE_FIELDS = ('unblock_date',)
USER_CAN_CHANGE_FIELDS = ('name', 'description', 'tags', 'is_private')


def check_fields_are_allowed(request: Request, allowed_fields: Tuple[str]) -> bool:
    for updated_field in request.data.keys():
        print(updated_field in request.data.keys())
        print(type(request.data))
        if updated_field not in allowed_fields:
            return False
    return True

def user_is_page_owner(request, obj):
    return request.user == obj.owner


def check_page_patch_permission(request, obj):
    if request.user.role == User.Roles.ADMIN:
        return check_fields_are_allowed(request, ADMIN_CAN_CHANGE_FIELDS)
    elif request.user.role == User.Roles.MODERATOR:
        return check_fields_are_allowed(request, MODERATOR_CAN_CHANGE_FIELDS)
    elif request.user.role == User.Roles.USER:
        return check_fields_are_allowed(request, USER_CAN_CHANGE_FIELDS) and user_is_page_owner(request, obj)
