from api.serializers.certificate_serializers import FavouriteSerializer
from docs.models import Favourite
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

User = get_user_model()


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
