from django.db.models import QuerySet
from rest_framework.request import Request
from users.models import User
from users.services.publisher import publish


def block_all_user_pages(pages: QuerySet) -> None:
    pages.update(is_blocked_forever=True)


def unblock_all_user_pages(pages: QuerySet) -> None:
    pages.update(is_blocked_forever=False)


def check_to_block_pages(request: Request) -> bool:
    return request.data.get("is_blocked")


def block_user_pages_service(user: User, request: Request) -> None:
    if "is_blocked" in request.data.keys():
        pages = user.pages.all()
        if check_to_block_pages(request):
            block_all_user_pages(pages)
        else:
            unblock_all_user_pages(pages)
