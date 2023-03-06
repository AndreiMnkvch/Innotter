from django.db.models import QuerySet
from rest_framework.request import Request
import json
from core.models import Tag, Page
from users.services.publisher import publish


class PageViewSetServices:

    @staticmethod
    def add_page_tag_service(page: Page, request: Request) -> None:
        for tag in request.data["tags"]:
            try:
                if page.tags.get(name__exact=tag["name"].strip().lower()):
                    continue
            except Tag.DoesNotExist:
                created_tag, created = Tag.objects.get_or_create(
                    name=tag["name"].strip().lower())
                page.tags.add(created_tag)

    @staticmethod
    def remove_page_tag_service(page: Page, request: Request) -> None:
        for tag in request.data["tags"]:
            try:
                tag_to_delete = page.tags.get(
                    name__exact=tag["name"].strip().lower())
                page.tags.remove(tag_to_delete)
            except Tag.DoesNotExist:
                pass

    @staticmethod
    def subscribe_service(page: Page, request: Request) -> None:
        if request.user not in page.followers.all():
            if page.is_private:
                page.follow_requests.add(request.user)
            else:
                page.followers.add(request.user)
                message = json.dumps({"user_id": page.owner.id, "page_uuid": str(
                    page.uuid), "follower_id": request.user.id})
                publish(message, "pages.update")

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
