from .models import Post, Page, Tag

from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ('is_blocked_forever', 'unblock_date', 'uuid')
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('likes',)
