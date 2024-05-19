from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework import permissions

from posts.models import Group, Post, Follow
from api.serializers import (GroupSerializer, PostSerializer,
                             CommentSerializer, FollowSerializer)
from .permissions import CustomPermission, ReadOnly


class UpdateDestroyMixin:
    """
    Миксин для обновления и удаления объектов.
    """
    def perform_update(self, serializer):
        """Обновляет существующий объект."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет существующий объект."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()


class ReadOnlyMixin:
    """
    Миксин для установки прав доступа только на чтение (GET).
    """
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class GroupViewSet(ReadOnlyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (CustomPermission,)


class PostViewSet(UpdateDestroyMixin, ReadOnlyMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    Создание, получение, обновление и удаление постов.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CustomPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(UpdateDestroyMixin, ReadOnlyMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления комментариями.
    Создание, получение, обновление и удаление комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = (CustomPermission,)

    def get_post(self):
        """
        Получает объект поста на основе идентификатора, переданного в URL.
        """
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        """
        Возвращает запрос для получения всех комментариев к указанному посту.
        """
        post = self.get_post()
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    """
     ViewSet для управления подписками.
    Создание, получение, обновление и удаление подписок пользователей.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        return self.request.user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
