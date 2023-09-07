from django.db import transaction
from rest_framework import serializers

from api.utils import Base64ImageField, create_thumbnail
from documents.models import Document, Element, Favourite, TextField


class FavouriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранные сертификаты."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favourite
        fields = ('user', 'certificate')


class TextFieldSerializer(serializers.ModelSerializer):
    """Текстовые поля документа(грамоты, сетрификата и др."""
    class Meta:
        model = TextField
        fields = ('text', 'coordinate_y', 'coordinate_x', 'font', 'font_size',
                  'font_color', 'is_bold', 'is_italic', 'text_decoration',
                  'align')


class ElementSerializer(serializers.ModelSerializer):
    """Элементы для документа: печать, факсимиле, лого и др."""
    image = Base64ImageField()

    class Meta:
        model = Element
        fields = ('coordinate_y', 'coordinate_x', 'image')


class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для превью документа(мини-версия)."""
    thumbnail = Base64ImageField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'thumbnail', 'category', 'color',
                  'is_horizontal')


class DocumentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор документа."""
    texts = TextFieldSerializer(many=True, required=False, read_only=True)
    elements = ElementSerializer(many=True, required=False, read_only=True)
    background = Base64ImageField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'thumbnail', 'background', 'category',
                  'color', 'is_horizontal', 'texts', 'elements')


class DocumentDetailWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания и записи документа в базу."""
    texts = TextFieldSerializer(many=True, required=False)
    elements = ElementSerializer(many=True, required=False)
    background = Base64ImageField()

    class Meta:
        model = Document
        fields = ('title', 'background', 'category',
                  'is_horizontal', 'texts', 'elements')

    @transaction.atomic
    def create(self, validated_data):
        texts = validated_data.pop('texts')
        elements = validated_data.pop('elements')
        document = Document.objects.create(**validated_data)
        for text in texts:
            TextField.objects.create(document=document, **text)
        for element in elements:
            Element.objects.create(document=document, **element)
        create_thumbnail(document)
        return document
