from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Group, Post, Follow


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    class Meta:
        model = Group
        fields = ('id', 'description', 'title', 'slug')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('text', 'pub_date', 'image', 'author', 'group', 'id')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'created', 'text',)
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username'
    )

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        user = self.context['request'].user
        if value == user:
            raise serializers.ValidationError('Выберите другого пользователя.')
        return value
