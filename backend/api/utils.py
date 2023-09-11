import base64
import os
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from documents.models import Font
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
        size = 192, 304
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
            ff = Font.objects.get(font=text.font, is_bold=text.is_bold,
                                  is_italic=text.is_italic)
            font = ImageFont.truetype(
                ff.font_file,
                text.font_size)
            draw.text(
                (text.coordinate_x + width, text.coordinate_y + height),
                text.text,
                font=font,
                fill=text.font_color)
            if text.text_decoration == 'underline':
                _, _, right, bottom = font.getbbox(text.text)
                underline_y = (text.coordinate_y + height
                               + (bottom - font.getmetrics()[1]) * 1.05)
                draw.line([
                    (text.coordinate_x + width, underline_y),
                    (text.coordinate_x + width + right, underline_y)],
                    fill=text.font_color,
                    width=2)
            if text.text_decoration == 'strikethrough':
                _, _, right, bottom = font.getbbox(text.text)
                strikethrough_y = (text.coordinate_y + height
                                   + (font.getmetrics()[0]
                                      - font.getmetrics()[1])
                                   )
                draw.line([
                    (text.coordinate_x + width, strikethrough_y),
                    (text.coordinate_x + width + right, strikethrough_y)],
                    fill=text.font_color,
                    width=2)
        im.thumbnail(size)
        thumb_io = BytesIO()
        im.save(thumb_io, 'JPEG', quality=95)
        document.thumbnail = File(
            thumb_io,
            name=os.path.basename(document.background.name))
        document.save()
