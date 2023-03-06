from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'is_blocked',
            'user_permissions',
            'groups',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'role',
            'last_login',
            'id'
        )

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class UserAdminSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        read_only_fields = ('date_joined', 'last_login', 'id', 'image_s3_path')


class UserModeratorSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        read_only_fields = (
            'id',
            'email',
            'image_s3_path',
            'role',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined',
            'last_login'
        )
