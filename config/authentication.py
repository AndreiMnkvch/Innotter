import jwt
from users.models import User
from rest_framework import authentication

from config import settings


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print('custom authentication is invoked')
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            access_token = auth_header.split()[1]
            print('access token from authentication:', access_token)
        else:
            print('No Authorization header provided in CustomAuthentication; return None')
            return None

        if access_token:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            user_id = payload["user_id"]
            print('user_id: ', user_id)
            user = User.objects.get(pk=user_id)
            return user, None
        return None
