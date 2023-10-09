import random

from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from documents.models import Document, Favourite, Font
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import User

from api.send_message.send_message import gmail_send_message
from api.serializers.certificate_serializers import (
    DocumentDetailSerializer, DocumentDetailWriteSerializer,
    DocumentSerializer, FavouriteSerializer, FontSerializer)
from api.serializers.user_serializers import (CodeValidationSerializer,
                                              MyUserCreateSerializer,
                                              RequestResetPasswordSerializer,
                                              ResetPasswordSerializer)

from .filters import DocumentFilter
from .utils import create_pdf
from django.core.mail import send_mail


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
        code = random.randint(1111, 9999)
        request.session['confirm_code'] = code
        request.session['confirm_email'] = email
        # gmail_send_message(code=code, email=email, activation=True)
        send_mail(
                    'Тема письма',
                    f'Ваш код для активации аккаунта {code}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {'Ошибка': 'Проверьте введенный email и/или пароль'},
        status=status.HTTP_400_BAD_REQUEST
    )


@swagger_auto_schema(method='POST',
                     request_body=RequestResetPasswordSerializer)
@api_view(['POST'])
def send_reset_code(request):
    'Генерация и отправка кода на почту для сброса пароля.'
    serializer = None
    if 'email' in request.data:
        email = request.data['email'].lower()
        serializer = RequestResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=email)
                code = random.randint(1111, 9999)
                request.session['recovery_code'] = code
                request.session['reset_email'] = email
                # gmail_send_message(code=code, email=user.email,
                #                    activation=False)
                send_mail(
                    'Тема письма',
                    f'Ваш код для сброса пароля {code}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                request.session['recovery_email_sent'] = True
            except User.DoesNotExist:
                return Response({'Ошибка': 'Пользователь с такой почтой не '
                                'существует.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'Ошибка': 'Отсутствует email в данных запроса.'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Код подтверждения отправлен на вашу почту.'},
                    status=status.HTTP_200_OK)



@swagger_auto_schema(method='POST', request_body=CodeValidationSerializer)
@api_view(['POST'])
def confirm_or_reset_code(request):
    """Подтверждение почты по коду или ввод кода для смены пароля."""
    serializer = CodeValidationSerializer(data=request.data)
    email = request.data.get('email')
    code = request.data.get('code')
    if serializer.is_valid():
        if 'recovery_code' in request.session:
            # Это запрос на ввод кода для смены пароля
            if (not request.session.get('recovery_email_sent')
                    or request.session.get('recovery_code_entered')):
                return Response({'message': 'Сначала отправьте письмо с кодом '
                                'восстановления'},
                                status=status.HTTP_400_BAD_REQUEST)
            code = serializer.validated_data['code']
            stored_code = request.session.get('recovery_code')
            if str(stored_code) == str(code):
                request.session['recovery_code_entered'] = True
                return Response({'message': 'Код восстановления принят'},
                                status=status.HTTP_200_OK)
            return Response({'Ошибка': 'Неверный код для смены пароля.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            # Это запрос на подтверждение почты
            confrim_code = request.session.get('confirm_code')
            email = request.session.get('confirm_email')
            if str(confrim_code) == str(code):
                user = User.objects.get(email=email)
                token = Token.objects.create(user=user)
                user.is_active = True
                user.save()
                return Response({'Token': str(token)},
                                status=status.HTTP_200_OK)
        return Response({'Ошибка': 'Отсутствует email в данных запроса или '
                        'неверный формат данных.'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'Ошибка': 'Проверьте код'},
                    status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=ResetPasswordSerializer)
@api_view(['POST'])
def reset_password(request):
    """Сброс пароля."""
    if not request.session.get('recovery_code_entered'):
        return Response({'message': 'Сначала введите код восстановления'},
                        status=status.HTTP_400_BAD_REQUEST)
    if 'new_password' in request.data and 're_new_password' in request.data:
        serializer = ResetPasswordSerializer(data=request.data)
        email = request.session.get('reset_email')
        if serializer.is_valid():
            password1 = serializer.validated_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            del request.session['recovery_email_sent']
            del request.session['recovery_code_entered']
            return Response({'message': 'Пароль успешно изменен.'},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Введите новый пароль и его подтверждение для '
                    'вашей учетной записи.'},
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
    serializer_class = FontSerializer
    queryset = Font.objects.all()
