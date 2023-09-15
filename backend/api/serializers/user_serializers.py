from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import User


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для обработки запросов на создание пользователя.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
        )


class MyUserSerializer(UserSerializer):
    """Cериализатор для получения юзера"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )


class ConfirmEmailSerializer(serializers.Serializer):
    """Сериализатор для подтверждения почты по коду"""
    email = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
