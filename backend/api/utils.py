import base64
import os
from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def create_thumbnail(document):
    if document.is_horizontal:
        size = 460, 304
    else:
        size = 304, 460
    with Image.open(document.background) as backgound:
        im = backgound.copy()
        width, height = im.size
        width /= 2
        height /= 2
        draw = ImageDraw.Draw(im)
        texts = document.textfield_set.all()
        for text in texts:
            font = ImageFont.truetype(
                os.path.join(settings.MEDIA_ROOT, 'fonts', 'arial.ttf'),
                text.font_size)
            draw.text(
                (text.coordinate_x + width, text.coordinate_y + height),
                text.text,
                font=font,
                fill='black')
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG', quality=95)
        document.thumbnail = File(
            thumb_io,
            name=os.path.basename(document.background.name))
        document.save()
