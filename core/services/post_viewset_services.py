from django.db.models import Q, QuerySet

from rest_framework.request import Request

from core.models import Page, Post


class PostViewSetServices:

    @staticmethod
    def list_service(request: Request) -> QuerySet:
        followed_pages = Page.objects.filter(Q(followers__id=request.user.id) | Q(owner__id=request.user.id))
        return Post.objects.filter(page__in=followed_pages).order_by('updated_at')

    @staticmethod
    def like_service(post: Post, request: Request) -> None:
        if post.likes.filter(id=request.user.id).exists():
            like = post.likes.get(id=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)

    @staticmethod
    def liked_posts_service(request: Request) -> QuerySet:
        return Post.objects.filter(likes__id=request.user.id)
