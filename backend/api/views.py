from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.send_message.send_message import gmail_send_message
from api.serializers.certificate_serializers import (
    DocumentDetailSerializer, DocumentDetailWriteSerializer,
    DocumentSerializer, FavouriteSerializer)
from api.serializers.user_serializers import (ConfirmEmailSerializer,
                                              MyUserCreateSerializer)
from documents.models import Document, Favourite

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


class FavouriteViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        if self.action == 'create':
            return DocumentDetailWriteSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=1)
        serializer.save(user=user)
