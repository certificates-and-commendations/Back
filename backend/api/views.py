from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
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
from .utils import create_pdf


@swagger_auto_schema(method='POST', request_body=MyUserCreateSerializer)
@api_view(['POST'])
def regist_user(request):
    """Регистрация пользователей"""
    serializer = MyUserCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
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


@swagger_auto_schema(method='POST', request_body=ConfirmEmailSerializer)
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
    """Избранное"""
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    """Документы"""
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DocumentFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocumentDetailSerializer
        if self.action in ('create', 'update'):
            return DocumentDetailWriteSerializer
        if self.action == 'favourite':
            return FavouriteSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        user = User.objects.get(id=1)
        serializer.save(user=user)

    @action(methods=['GET',], detail=True)
    def download(self, request, pk):
        document = Document.objects.get(id=pk)
        b = create_pdf(document)
        return FileResponse(b, as_attachment=True, filename="hello.pdf")

    @action(methods=['DELETE', 'POST'], detail=True,
            permission_classes=[IsAuthenticated])
    def favourite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            serializer = self.get_serializer(
                data={'user': user.id, 'document': pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        Favourite.objects.filter(user=user, document=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FontViewSet(viewsets.ModelViewSet):
    """Шрифты"""
    serializer_class = FontSerializer
    queryset = Font.objects.all()
