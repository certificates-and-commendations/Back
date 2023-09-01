from api.send_message.send_message import gmail_send_message
from api.serializers.certificate_serializers import FavouriteSerializer
from api.serializers.user_serializers import ConfirmEmailSerializer
from api.serializers.user_serializers import MyUserCreateSerializer
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from docs.models import Favourite
from rest_framework import mixins
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import User

User = get_user_model()


@api_view(['POST'])
def regist_user(request):
    """Регистрация пользователей"""
    serializer = MyUserCreateSerializer(data=request.data)
    if User.objects.filter(
            email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    if serializer.is_valid():
        serializer.save()
        # Отправка кода на почту
        code = serializer.data.get('code')
        gmail_send_message(code=code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirm_code(request):
    """Подтверждение почты по коду"""
    serializer = ConfirmEmailSerializer(data=request.data)
    user = User.objects.get(email=request.data.get('email'))
    code = request.data.get('code')
    if serializer.is_valid():
        if str(user.code) == str(code):
            # Создание токена
            token = Token.objects.create(user=user)
            return Response({'Token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(DjoserUserViewSet):
    """Убирает не используемые @action из user view"""
    activation = None
    resend_activation = None
    reset_password = None
    reset_password_confirm = None
    set_username = None
    reset_username = None
    reset_username_confirm = None


class FavouriteViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
