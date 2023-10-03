from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
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


class RequestResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для отправки кода на почту для сброса пароля."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)
        except ValidationError:
            raise serializers.ValidationError('Неверный формат адреса '
                                              'электронной почты.')
        return value


class CodeValidationSerializer(serializers.Serializer):
    """Сериализатор для проверки кода."""
    code = serializers.CharField(max_length=4)


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""
    password1 = serializers.CharField(
        min_length=8,
        write_only=True,
    )
    password2 = serializers.CharField(
        write_only=True,
    )

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        try:
            password_validation.validate_password(data['password1'])
        except password_validation.ValidationError as error:
            raise serializers.ValidationError({'password1': error.messages})
        return data
