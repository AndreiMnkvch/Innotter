import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from config import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('request.headers', request.headers)
        print('request.path', request.path)
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            print('No auth header so request.user:', request.user)
            response = self.get_response(request)

        else:
            auth_header_parts = auth_header.split()
            if len(auth_header_parts) != 2:
                return HttpResponse(f"Authorization header consist of {len(auth_header_parts)} parts."
                             f" But should be 2! Check it out", status=401)

            access_token = auth_header_parts[1]
            print('access token:', access_token)

            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
                user_id = payload["user_id"]
                response = self.get_response(request)
            except jwt.ExpiredSignatureError:
                HttpResponse('Access token is expired!', status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                HttpResponse('Invalid access token! Please send valid token', status=401)

        return response