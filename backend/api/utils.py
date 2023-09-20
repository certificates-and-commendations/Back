import base64
import os
from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from documents.models import Font
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from rest_framework import serializers
from reportlab.lib.styles import ParagraphStyle


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def image_draw(background, elements):
    background_im = Image.open(background)
    width, height = background_im.size
    im = Image.new('RGBA', size=(width, height))
    im.paste(background_im)
    width //= 2
    height //= 2
    for element in elements:
        with Image.open(element.image) as foreground:
            foreground = foreground.convert('RGBA')
            im.paste(foreground, (element.coordinate_x + int(width),
                                  element.coordinate_y + int(height)),
                     foreground)
    return im


def create_thumbnail(document):
    if document.is_horizontal:
        size = 304, 192
    else:
        size = 304, 460
    im = image_draw(document.background, document.element_set.all())
    width, height = im.size
    width /= 2
    height /= 2
    draw = ImageDraw.Draw(im)
    texts = document.textfield_set.all()
    for text in texts:
        ff = Font.objects.get(font=text.font, is_bold=text.is_bold,
                              is_italic=text.is_italic)
        font = ImageFont.truetype(ff.font_file, text.font_size)
        draw.text((text.coordinate_x + width, text.coordinate_y + height),
                  text.text, font=font, fill=text.font_color, align=text.align)
        if text.text_decoration == 'none':
            continue
        _, _, right, bottom = font.getbbox(text.text)
        if text.text_decoration == 'underline':
            line_y = (text.coordinate_y + height
                      + (bottom - font.getmetrics()[1]) * 1.05)
        if text.text_decoration == 'strikethrough':
            line_y = (text.coordinate_y + height + (font.getmetrics()[0]
                                                    - font.getmetrics()[1]))
        draw.line([
            (text.coordinate_x + width, line_y),
            (text.coordinate_x + width + right, line_y)],
            fill=text.font_color, width=2)
    im = im.convert('RGB')
    im_resized = im.resize(size)
    thumb_io = BytesIO()
    im_resized.save(thumb_io, 'JPEG', quality=95)
    document.thumbnail = File(thumb_io,
                              name=os.path.basename(document.background.name))
    document.save()


def create_pdf(document):
    buffer = BytesIO()
    background = image_draw(document.background, document.element_set.all())
    doc_width, doc_height = background.size
    canvas = Canvas(buffer, pagesize=background.size)
    width = doc_width / 2
    height = doc_height / 2
    canvas.drawImage(ImageReader(background), 0, 0)
    texts = document.textfield_set.all()
    for text in texts:
        font = Font.objects.get(font=text.font, is_bold=text.is_bold,
                                is_italic=text.is_italic)
        pdfmetrics.registerFont(TTFont(font.font, font.font_file.path))
        face = pdfmetrics.getFont(font.font).face
        string_height = (face.ascent - face.descent) / 1000 * text.font_size
        style = ParagraphStyle(
            name='custom',
            fontName=font.font,
            fontSize=text.font_size,
            textColor=text.font_color)
        decoration = {
            'underline': f'<u>{text.text}</u>',
            'strikethrough': f'<strike>{text.text}</strike>',
            'none': f'{text.text}',
        }
        paragraph = Paragraph(decoration[text.text_decoration], style)
        string_width = stringWidth(text.text, font.font, text.font_size)
        paragraph.wrapOn(canvas, string_width, string_height)
        paragraph.drawOn(canvas, text.coordinate_x + width,
                         doc_height - text.coordinate_y - height)
    canvas.showPage()
    canvas.save()
    buffer.seek(0)
    return buffer
