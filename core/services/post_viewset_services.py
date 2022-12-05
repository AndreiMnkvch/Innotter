from django.db.models import Q
from rest_framework.response import Response

from core.models import Page, Post
from core.serializers import PostSerializer


def list_service(self, request):
    followed_pages = Page.objects.filter(Q(followers__id=request.user.id) | Q(owner__id=request.user.id))
    queryset = Post.objects.filter(page__in=followed_pages).order_by('updated_at')
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)

def like_service(self, request, pk=None):
    post = self.get_object()
    if post.likes.filter(id=request.user.id).exists():
        like = post.likes.get(id=request.user.id)
        post.likes.remove(like)
    else:
        post.likes.add(request.user)
    return Response(data='success', status=200)

def liked_posts_service(self, request):
    liked_posts = Post.objects.filter(likes__id=request.user.id)
    serializer = PostSerializer(liked_posts, many=True)
    return Response(serializer.data)
