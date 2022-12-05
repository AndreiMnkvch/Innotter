from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Page, Tag, Post
from .permissions import PagePermission, PostPermission
from .serializers import PageSerializer, PostSerializer, TagSerializer

from .services.page_viewset_services import add_page_tag_service, \
    remove_page_tag_service, subscribe_service, \
    follow_requests_service, \
    approve_follow_requests_service, \
    decline_follow_requests_service

from .services.post_viewset_services import list_service, like_service, liked_posts_service


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (PagePermission, IsAuthenticated)

    @action(methods=['patch', ], detail=True)
    def add_page_tag(self, request, pk=None):
        return add_page_tag_service(self, request, pk=None)

    @action(methods=['patch', ], detail=True)
    def remove_page_tag(self, request, pk=None):
        return remove_page_tag_service(self, request, pk=None)

    @action(methods=['patch', ], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        return subscribe_service(self, request, pk=None)

    @action(detail=True)
    def follow_requests(self, request, pk=None):
        return follow_requests_service(self, request, pk=None)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def approve_follow_requests(self, request, pk=None):
        approve_follow_requests_service(self, request, pk=None)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def decline_follow_requests(self, request, pk=None):
        decline_follow_requests_service(self, request, pk=None)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, PostPermission)

    def list(self, request):
        return list_service(self, request)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        like_service(self, request, pk=None)

    @action(detail=False)
    def liked_posts(self, request):
        return liked_posts_service(self, request)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)
