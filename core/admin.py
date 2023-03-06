from django.contrib import admin
from .models import Tag, Page, Post


class PageAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'description', 'tags',
                       'owner', 'followers', 'image', 'is_private']


admin.site.register(Tag)
admin.site.register(Page, PageAdmin)
admin.site.register(Post)
