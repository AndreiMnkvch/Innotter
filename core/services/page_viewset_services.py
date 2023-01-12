from django.db.models import QuerySet

from rest_framework.request import Request

from core.models import Tag, Page


class PageViewSetServices:

    @staticmethod
    def add_page_tag_service(page: Page, request: Request) -> None:
        for tag in request.data["tags"]:
            try:
                if page.tags.get(name__iexact=tag["name"]):
                    continue
            except Tag.DoesNotExist:
                created_tag, created = Tag.objects.get_or_create(name=tag["name"].lower())
                page.tags.add(created_tag)

    @staticmethod
    def remove_page_tag_service(page: Page, request: Request) -> None:
        for tag in request.data["tags"]:
            try:
                tag_to_delete = page.tags.get(name__exact=tag["name"])
                page.tags.remove(tag_to_delete)
            except Tag.DoesNotExist:
                pass

    @staticmethod
    def subscribe_service(page: Page, request: Request) -> None:
        if page.is_private:
            page.follow_requests.add(request.user)
        else:
            page.followers.add(request.user)

    @staticmethod
    def follow_requests_service(page: Page) -> QuerySet:
        return page.follow_requests.all()

    @staticmethod
    def approve_follow_requests_service(page: Page) -> None:
        follow_requests = page.follow_requests.all()
        for follow_request in follow_requests:
            page.followers.add(follow_request)
            page.follow_requests.remove(follow_request)

    @staticmethod
    def decline_follow_requests_service(page: Page) -> None:
        follow_requests = page.follow_requests.all()
        for follow_request in follow_requests:
            page.follow_requests.remove(follow_request)
