from django.db.models import Q, QuerySet
from rest_framework.request import Request
from core.models import Page, Post
import json
import boto3
import botocore
from users.services.publisher import publish


class PostViewSetServices:

    @staticmethod
    def list_service(request: Request) -> QuerySet:
        followed_pages = Page.objects.filter(
            Q(followers__id=request.user.id) | Q(owner__id=request.user.id))
        return Post.objects.filter(page__in=followed_pages).order_by('updated_at')

    @staticmethod
    def like_service(post: Post, request: Request) -> None:
        if post.likes.filter(id=request.user.id).exists():
            like = post.likes.get(id=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)
            print(post.likes.all())
            message = json.dumps(
                {
                    "post_id": post.id,
                    "user_id": post.page.owner.id,
                    "page_uuid": str(post.page.uuid),
                    "liked_user_id": request.user.id
                }
            )
            publish(message, "posts.liked")

    @staticmethod
    def liked_posts_service(request: Request) -> QuerySet:
        return Post.objects.filter(likes__id=request.user.id)


def get_post_page_followers_emails(instance: Post) -> list[str]:
    return [i[0] for i in instance.page.followers.all().values_list('email')]


def send_new_post_notification_service(new_post: Post, followers_email_list: list[str]):
    test_source_email = 'justaandrew@gmail.com'
    template_name = 'New_Post_Notification'
    client = boto3.client('ses')
    try:
        client.get_template(TemplateName=template_name)
    except botocore.exceptions.ClientError:
        client.create_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': 'Post_Notification',
                'TextPart': 'Page {{page}} has a new post! Check it out!',
                'HtmlPart': ''
            })
    client.send_templated_email(
        Source=test_source_email,
        Template=template_name,
        Destination={
            'ToAddresses': followers_email_list
        },
        TemplateData=json.dumps({"page": new_post.page.name})
    )
