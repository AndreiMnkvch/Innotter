from django.contrib import admin
from .models import Tag, Page, Post
    
admin.site.register(Tag)
admin.site.register(Page)
admin.site.register(Post)

# Register your models here.
