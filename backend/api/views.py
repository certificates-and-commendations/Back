from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.send_message.send_message import gmail_send_message
from api.serializers.certificate_serializers import (
    DocumentDetailSerializer, DocumentDetailWriteSerializer,
    DocumentSerializer, FavouriteSerializer, FontSerializer)
from api.serializers.user_serializers import (ConfirmEmailSerializer,
                                              MyUserCreateSerializer)
from documents.models import Document, Favourite, Font
from .filters import DocumentFilter
from users.models import User


@api_view(['POST'])
def regist_user(request):
    """Регистрация пользователей"""
    serializer = MyUserCreateSerializer(data=request.data)
    if User.objects.filter(
            email=request.data.get('email')
    ).exists():
        return Response(
            {'Ошибка': 'Пользователь с таким email уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if serializer.is_valid():
        serializer.save()
        email = serializer.data.get('email')
        user = User.objects.get(email=email)
        user.is_active = False
        # Отправка кода на почту
        code = user.code
        gmail_send_message(code=code, email=email)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(
        {'Ошибка': 'Проверьте введенный email и/или пароль'},
        status=status.HTTP_400_BAD_REQUEST
    )


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
            user.is_active = True
            user.save()
            return Response({'Token': str(token)}, status=status.HTTP_200_OK)

    return Response({'Ошибка': 'Проверьте код'},
                    status=status.HTTP_400_BAD_REQUEST)


class FavouriteViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DocumentFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        if self.action == 'create':
            return DocumentDetailWriteSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=1)
        serializer.save(user=user)


class FontViewSet(viewsets.ModelViewSet):
    serializer_class = FontSerializer
    queryset = Font.objects.all()
