import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from django.forms import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class MyUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для обработки запросов на создание пользователя.
    Валидирует создание пользователя с юзернеймом 'me'."""
    avatar_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar_image',
            'password',
        )

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return lower_email

    def validate_username(self, value):
        lower_username = value.lower()
        if User.objects.filter(username__iexact=lower_username).exists():
            raise ValidationError(
                'Пользователь с таким username уже зарегистрирован'
            )
        if value == "me":
            raise ValidationError(
                'Невозможно создать пользователя с таким именем!'
            )
        return lower_username


class MyUserSerializer(UserSerializer):
    """сериализатор для получения юзера"""

    avatar_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar_image',
        )
