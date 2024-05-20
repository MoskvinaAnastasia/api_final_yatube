from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from .constants import API_VERSION

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comments')
router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(f'{API_VERSION}/', include(router_v1.urls)),
    path(f'{API_VERSION}/', include('djoser.urls')),
    path(f'{API_VERSION}/', include('djoser.urls.jwt')),
]
