from django.core.validators import validate_image_file_extension
from django.db import models
import uuid


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.UUIDField(max_length=30, primary_key=True, unique=True, default=uuid.uuid4())
    description = models.TextField()
    tags = models.ManyToManyField('core.Tag', related_name='pages', blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', related_name='follows', blank=True)
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to='page_images',
                              validators=[validate_image_file_extension]
                              )
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', blank=True, related_name='requests')
    is_blocked_forever = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    page = models.ForeignKey('core.Page', on_delete=models.CASCADE, related_name='posts', db_column='uuid')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('core.Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField('users.User', blank=True, related_name='liked_posts')

    def __str__(self):
        return f'post id={self.id} of page {self.page}'
