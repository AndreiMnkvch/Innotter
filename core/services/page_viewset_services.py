from rest_framework.response import Response

from core.models import Tag
from users.serializers import UserSerializer


def add_page_tag_service(self, request, pk=None):
    page = self.get_object()
    for tag in request.data["tags"]:
        try:
            if page.tags.get(name__iexact=tag["name"]):
                continue
        except Tag.DoesNotExist:
            created_tag, created = Tag.objects.get_or_create(name=tag["name"].lower())
            page.tags.add(created_tag)
    return Response(data='success', status=201)

def remove_page_tag_service(self, request, pk=None):
    page = self.get_object()
    for tag in request.data["tags"]:
        try:
            tag_to_delete = page.tags.get(name__exact=tag["name"])
        except Tag.DoesNotExist:
            page.tags.remove(tag_to_delete)
    return Response(data='success tag is deleted', status=200)

def subscribe_service(self, request, pk=None):
    page = self.get_object()
    if page.is_private:
        page.follow_requests.add(request.user)
    else:
        page.followers.add(request.user)
    return Response(data='success', status=200)

def follow_requests_service(self, request, pk=None):
    page = self.get_object()
    follow_requests = page.follow_requests.all()
    serializer = UserSerializer(follow_requests, many=True)
    return Response(serializer.data)

def approve_follow_requests_service(self, request, pk=None):
    page = self.get_object()
    follow_requests = page.follow_requests.all()
    for follow_request in follow_requests:
        page.followers.add(follow_request)
        page.follow_requests.remove(follow_request)
    return Response('ok')

def decline_follow_requests_service(self, request, pk=None):
    page = self.get_object()
    follow_requests = page.follow_requests.all()
    for follow_request in follow_requests:
        page.follow_requests.remove(follow_request)
    return Response('ok')
