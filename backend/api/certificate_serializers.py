from docs.models import Favourite
from rest_framework import serializers


class FavouriteSerializer(serializers.ModelSerializer):
    """Сериализатор сертификатов"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favourite
        fields = ('user', 'certificate')
