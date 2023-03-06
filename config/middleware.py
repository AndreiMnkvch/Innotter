import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from config import settings


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            response = self.get_response(request)

        else:
            auth_header_parts = auth_header.split()
            if len(auth_header_parts) != 2:
                return HttpResponse(f"Authorization header consist of {len(auth_header_parts)} parts."
                             f" But should be 2! Check it out", status=401)

            access_token = auth_header_parts[1]
            print('access token:', access_token)

            try:
                jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            except jwt.ExpiredSignatureError:
                return HttpResponse('Access token is expired!', status=401)
            except (jwt.exceptions.DecodeError, jwt.InvalidTokenError):
                return HttpResponse('Invalid access token! Please send valid token', status=401)
            response = self.get_response(request)

        return response
