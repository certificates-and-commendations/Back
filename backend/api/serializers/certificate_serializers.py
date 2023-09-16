from api.utils import Base64ImageField, create_thumbnail
from django.db import transaction
from documents.models import Document, Element, Favourite, Font, TextField
from fontTools import ttLib
from rest_framework import serializers


class FavouriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранные сертификаты"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favourite
        fields = ('user', 'document')


class FontSerializer(serializers.ModelSerializer):
    """Сериализатор шрифта"""
    class Meta:
        model = Font
        fields = ('id', 'font', 'is_bold', 'is_italic', 'font_file')
        read_only_fields = ('id', 'font', 'is_bold', 'is_italic')

    def create(self, validated_data):
        tt = ttLib.TTFont(validated_data['font_file'])
        subfamily = tt['name'].getDebugName(2)
        font, created = Font.objects.get_or_create(
            font=tt['name'].getDebugName(1),
            is_bold=('Bold' in subfamily),
            is_italic=('Italic' in subfamily)
        )
        if created:
            font.font_file = validated_data['font_file']
            font.save()
        return font


class TextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextField
        fields = ('text', 'coordinate_y', 'coordinate_x', 'font', 'font_size',
                  'font_color', 'is_bold', 'is_italic', 'text_decoration',
                  'align')


class ElementSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Element
        fields = ('coordinate_y', 'coordinate_x', 'image')


class DocumentSerializer(serializers.ModelSerializer):
    thumbnail = Base64ImageField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'thumbnail', 'category', 'color',
                  'is_horizontal')


class DocumentDetailSerializer(serializers.ModelSerializer):
    texts = TextFieldSerializer(
        source='textfield_set',
        many=True,
        required=False)
    elements = ElementSerializer(
        source='element_set',
        many=True,
        required=False)
    background = Base64ImageField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'background', 'category', 'color',
                  'is_horizontal', 'texts', 'elements')


class DocumentDetailWriteSerializer(serializers.ModelSerializer):
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
