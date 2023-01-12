from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Post
from core.tasks import send_new_post_notification_task

@receiver(post_save, sender=Post)
def post_notification_handler(instance: Post, **kwargs):
    send_new_post_notification_task.delay(instance.pk)
