import jwt
from users.models import User
from rest_framework import authentication

from config import settings


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            access_token = auth_header.split()[1]
        else:
            return None

        if access_token:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            user_id = payload["user_id"]
            user = User.objects.get(pk=user_id)
            return user, None
        return None
