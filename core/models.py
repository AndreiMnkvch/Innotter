from django.core.validators import validate_image_file_extension
from django.db import models
import uuid
import json
from users.services.publisher import publish


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.UUIDField(
        max_length=30, primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    tags = models.ManyToManyField('core.Tag', related_name='pages', blank=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField(
        'users.User', related_name='follows', blank=True)
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to='page_images',
                              validators=[validate_image_file_extension]
                              )
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        'users.User', blank=True, related_name='requests')
    is_blocked_forever = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        message = json.dumps(
            {"page_uuid": str(self.uuid), "user_id": self.owner.id})
        publish(message, "pages.create")

    def delete(self, *args, **kwargs):
        message = json.dumps(
            {"page_uuid": str(self.uuid), "user_id": self.owner.id})
        super().delete(*args, **kwargs)
        publish(message, "pages.delete")


class Post(models.Model):
    page = models.ForeignKey(
        'core.Page', on_delete=models.CASCADE, related_name='posts', db_column='uuid')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey(
        'core.Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        'users.User', blank=True, related_name='liked_posts')

    def __str__(self):
        return f'post id={self.id} of page {self.page}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        message = json.dumps(
            {
                "post_id": self.id,
                "page_uuid": str(self.page.uuid),
                "user_id": self.page.owner.id
            }
        )
        publish(message, "posts.create")

    def delete(self, *args, **kwargs):
        message = json.dumps(
            {
                "post_id": self.id,
                "page_uuid": str(self.page.uuid),
                "user_id": self.page.owner.id
            }
        )
        super().delete(*args, **kwargs)
        publish(message, "posts.delete")
