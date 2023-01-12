from config.celery import app
from core.models import Post
from core.services.post_viewset_services import get_post_page_followers_emails, send_new_post_notification_service


@app.task
def send_new_post_notification_task(instance_id):
    new_post = Post.objects.get(pk=instance_id)
    followers_email_list = get_post_page_followers_emails(new_post)
    send_new_post_notification_service(new_post, followers_email_list)
