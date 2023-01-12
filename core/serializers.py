from .models import Post, Page, Tag

from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageBaseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ('is_blocked_forever', 'unblock_date', 'uuid')
        depth = 1

class PageAdminSerializer(PageBaseSerializer):
    class Meta(PageBaseSerializer.Meta):
        read_only_fields = ('name', 'description', 'tags', 'followers','image','is_private', 'uuid')

class PageModeratorSerializer(PageBaseSerializer):
    class Meta(PageBaseSerializer.Meta):
        read_only_fields = ('name', 'is_blocked_forever', 'description', 'tags', 'followers','image','is_private', 'uuid')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('likes',)
