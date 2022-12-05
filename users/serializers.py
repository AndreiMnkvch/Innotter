from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('user_permissions',
                            'groups',
                            'is_blocked',
                            'is_superuser',
                            'is_staff',
                            'is_active',
                            'date_joined',
                            'role',
                            'last_login',
                            'id')


    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)
