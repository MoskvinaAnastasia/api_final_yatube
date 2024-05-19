from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Follow
from api.serializers import (GroupSerializer, PostSerializer,
                             CommentSerializer, FollowSerializer)
from .permissions import CustomPermission


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


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления постами.
    Создание, получение, обновление и удаление постов.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (CustomPermission,)

    def perform_create(self, serializer):
        """Создает новый пост."""
        serializer.save(author=self.request.user)


class CommentViewSet(UpdateDestroyMixin, viewsets.ModelViewSet):
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
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (CustomPermission,)
