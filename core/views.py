from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.services.publisher import publish
from users.serializers import UserBaseSerializer
from core.models import Page, Tag, Post
from core.permissions import PagePermission, PageOwner, PostPermission
from core.serializers import PageBaseSerializer, PostSerializer, TagSerializer
from core.services.page_viewset_services import PageViewSetServices
from core.services.post_viewset_services import PostViewSetServices


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageBaseSerializer
    permission_classes = (IsAuthenticated, PagePermission)

    @action(methods=['patch'], detail=True)
    def add_page_tag(self, request, pk=None):
        page = self.get_object()
        PageViewSetServices.add_page_tag_service(page, request)
        return Response(status=200)

    @action(methods=['patch'], detail=True)
    def remove_page_tag(self, request, pk=None):
        page = self.get_object()
        PageViewSetServices.remove_page_tag_service(page, request)
        return Response(status=200)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        page = self.get_object()
        PageViewSetServices.subscribe_service(page, request)
        return Response(status=200)

    @action(detail=True, permission_classes=[PageOwner])
    def follow_requests(self, request, pk=None):
        page = self.get_object()
        follow_requests = PageViewSetServices.follow_requests_service(page)
        serializer = UserBaseSerializer(follow_requests, many=True)
        return Response(serializer.data, status=200)

    @action(methods=['patch'], detail=True, permission_classes=[PageOwner])
    def approve_follow_requests(self, request, pk=None):
        page = self.get_object()
        PageViewSetServices.approve_follow_requests_service(page)
        return Response(status=200)

    @action(methods=['patch'], detail=True, permission_classes=[PageOwner])
    def decline_follow_requests(self, request, pk=None):
        page = self.get_object()
        PageViewSetServices.decline_follow_requests_service(page)
        return Response(status=200)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, PostPermission)

    def list(self, request):
        queryset = PostViewSetServices.list_service(request)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated], url_name="like")
    def like(self, request, pk=None):
        post = self.get_object()
        PostViewSetServices.like_service(post, request)
        return Response(status=200)

    @action(detail=False)
    def liked_posts(self, request):
        liked_posts = PostViewSetServices.liked_posts_service(request)
        serializer = PostSerializer(liked_posts, many=True)
        return Response(serializer.data, status=200)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
