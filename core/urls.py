from django.urls import path, include
from rest_framework import routers
from core.views import TagViewSet, PostViewSet, PageViewSet

router = routers.DefaultRouter()

router.register(r'tag', TagViewSet)
router.register(r'post', PostViewSet)
router.register(r'page', PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
