from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, exceptions
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .permissions import UserPermission
from .serializers import UserBaseSerializer, UserAdminSerializer, UserModeratorSerializer
from .models import User
from .services.token_services import generate_access_token, generate_refresh_token
from .services.user_viewset_services import block_user_pages_service


class UserViewSet(viewsets.ModelViewSet):
    """
        A simple ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = [UserPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def get_serializer_class(self):
        try:
            match self.request.user.role:
                case User.Roles.ADMIN:
                    return UserAdminSerializer
                case User.Roles.MODERATOR:
                    return UserModeratorSerializer
                case User.Roles.USER:
                    return UserBaseSerializer
        except AttributeError:
            return UserBaseSerializer

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        block_user_pages_service(user, request)
        return super().partial_update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    print(request.user)
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserBaseSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response
