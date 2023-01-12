from django.core.validators import validate_image_file_extension
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image_s3_path = models.ImageField(null=True,
                                      blank=True,
                                      upload_to='user_images',
                                      validators=[validate_image_file_extension]
                                      )
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username
