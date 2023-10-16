from api.utils import Base64ImageField, create_thumbnail, dominant_color
from django.core.validators import FileExtensionValidator
from django.db import transaction
from documents.models import (Document, Element, Favourite,
                              Font, TemplateColor, TextField)
from fontTools import ttLib
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class FavouriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранные сертификаты"""
    class Meta:
        model = Favourite
        fields = ('user', 'document')
        extra_kwargs = {
            'user': {'write_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Favourite.objects.all(),
                fields=['user', 'document']
            )
        ]


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


class FontInTextSerializer(serializers.ModelSerializer):
    """Сериализатор шрифта"""

    class Meta:
        model = Font
        fields = ('font', 'is_bold', 'is_italic')


class TextFieldSerializer(serializers.ModelSerializer):
    """Сериализатор для TextField"""
    font = FontInTextSerializer()

    class Meta:
        model = TextField
        fields = (
            'id', 'text', 'coordinate_y', 'coordinate_x', 'font',
            'font_size', 'font_color', 'text_decoration', 'align'
        )
        read_only_fields = ('id',)


class ElementSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Element
        fields = ('coordinate_y', 'coordinate_x', 'image')


class IsFavouriteField(serializers.SerializerMethodField):
    def to_representation(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.favourite.filter(document=obj.id).exists()


class DocumentSerializer(serializers.ModelSerializer):
    thumbnail = Base64ImageField()
    is_favourite = IsFavouriteField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'thumbnail', 'category', 'color',
                  'is_horizontal', 'is_favourite')


class ShortDocumentSerializer(serializers.ModelSerializer):
    thumbnail = Base64ImageField()
    is_favourite = IsFavouriteField()

    class Meta:
        model = Document
        fields = ('id', 'thumbnail', 'is_favourite')


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
        fields = ('id', 'user', 'title', 'background', 'category', 'color',
                  'is_horizontal', 'texts', 'elements')


class DocumentDetailWriteSerializer(serializers.ModelSerializer):
    texts = TextFieldSerializer(many=True, required=False)
    elements = ElementSerializer(many=True, required=False)
    background = Base64ImageField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'background', 'category',
                  'is_horizontal', 'texts', 'elements')
        read_only_fields = ('id',)

    def create_texts_elements(self, document, texts, elements):
        for text in texts:
            font_data = text.pop('font')
            font = Font.objects.get(**font_data)
            TextField.objects.create(document=document, font=font, **text)

        for element in elements:
            Element.objects.create(document=document, **element)

        colors = dominant_color(document.background)
        for color in colors:
            document.color.add(color)
        create_thumbnail(document)

    @transaction.atomic
    def create(self, validated_data):
        texts = []
        elements = []
        if 'texts' in validated_data:
            texts = validated_data.pop('texts')
        if 'elements' in validated_data:
            elements = validated_data.pop('elements')
        document = Document.objects.create(**validated_data)
        self.create_texts_elements(document, texts, elements)
        return document

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.textfield_set.all().delete()
        instance.element_set.all().delete()
        instance.documentcolor_set.all().delete()
        texts = []
        elements = []
        if 'texts' in validated_data:
            texts = validated_data.pop('texts')
        if 'elements' in validated_data:
            elements = validated_data.pop('elements')
        self.create_texts_elements(instance, texts, elements)
        return super().update(instance=instance, validated_data=validated_data)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateColor
        fields = ('__all__')


class FileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])
