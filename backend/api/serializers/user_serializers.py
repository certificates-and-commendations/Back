from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from api.utils import Base64ImageField
from users.models import User


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для обработки запросов на создание пользователя.
    Валидирует создание пользователя с юзернеймом 'me'."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar_image',
            'password',
            'code'
        )


class MyUserSerializer(UserSerializer):
    """сериализатор для получения юзера"""

    avatar_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'code',
            'avatar_image',
        )


class ConfirmEmailSerializer(serializers.Serializer):
    """Сериализатор для подтверждения почты по коду"""
    email = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
