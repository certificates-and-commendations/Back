from django.contrib.auth import password_validation
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


class RequestResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для отправки кода на почту для сброса пароля."""
    email = serializers.EmailField(required=True)


class CodeValidationSerializer(serializers.Serializer):
    """Сериализатор для проверки кода."""
    code = serializers.CharField(max_length=4)


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    new_password = serializers.CharField(
        min_length=8,
        write_only=True,
    )
    re_new_password = serializers.CharField(
        write_only=True,
    )

    def validate(self, data):
        if data['new_password'] != data['re_new_password']:
            raise serializers.ValidationError('Пароли не совпадают')
        try:
            password_validation.validate_password(data['new_password'])
        except password_validation.ValidationError as error:
            raise serializers.ValidationError({'new_password': error.messages})
        return data
