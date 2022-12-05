from rest_framework import viewsets
from rest_framework.permissions import *

from .permissions import UserPermission
from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
        A simple ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BasePermission, UserPermission]
