from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet
from .constants import API_VERSION

router_v1 = DefaultRouter()
router_v1.register('posts', PostViewSet, basename='posts')
router_v1.register('groups', GroupViewSet, basename='groups')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path(f'api/{API_VERSION}/api-token-auth/', obtain_auth_token),
    path(f'{API_VERSION}/', include(router_v1.urls)),
]
