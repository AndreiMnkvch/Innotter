from django.urls import path, include
from rest_framework import routers
from core.views import TagViewSet, PostViewSet, PageViewSet

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'pages', PageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
