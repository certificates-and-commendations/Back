from django.core.management.base import BaseCommand
from django.db import IntegrityError
from documents.models import Font, Document, TextField
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        headers = ['font', 'is_bold', 'is_italic', 'font_file']
        fonts = (
            ('Arial', False, False, 'fonts/Arial.ttf'),
            ('Arial', True, False, 'fonts/Arial Bold.ttf'),
            ('Arial', False, True, 'fonts/Arial Italic.ttf'),
            ('Arial', True, True, 'fonts/Arial Bold Italic.ttf'),
            ('Montserrat', False, False, 'fonts/Montserrat-Regular.ttf'),
            ('Montserrat', True, False, 'fonts/Montserrat-Bold.ttf'),
            ('Montserrat', False, True, 'fonts/Montserrat-Italic.ttf'),
            ('Montserrat', True, True, 'fonts/Montserrat-BoldItalic.ttf'),
            ('Roboto', False, False, 'fonts/Roboto-Regular.ttf'),
            ('Roboto', True, False, 'fonts/Roboto-Bold.ttf'),
            ('Roboto', False, True, 'fonts/Roboto-Italic.ttf'),
            ('Roboto', True, True, 'fonts/Roboto-BoldItalic.ttf'),
            ('WixMadeforDisplay', False, False,
             'fonts/WixMadeforDisplay-Regular.ttf'),
            ('WixMadeforDisplay', True, False,
             'fonts/WixMadeforDisplay-Bold.ttf'),
            ('Times New Roman', False, False, 'fonts/Times New Roman.ttf'),
            ('Times New Roman', True, False, 'fonts/Times New Roman Bold.ttf'),
            ('Times New Roman', False, True,
             'fonts/Times New Roman Italic.ttf'),
            ('Times New Roman', True, True,
             'fonts/Times New Roman Bold Italic.ttf'),
        )
        for font in fonts:
            f = dict(zip(headers, font))
            Font.objects.get_or_create(**f)

        # Users
        for i in range(3):
            try:
                user = User.objects.create_user(
                    email=f'mail{i}@mail.com',
                    password='Passw0rd!')
                user.is_active = 1
                user.save()
            except IntegrityError:
                self.stdout.write(f'user {i} already exists')

        # Docs
        font = Font.objects.get(id=1)
        texts_vertical = (
            ('Грамота', -174, -146, font, 94, '#000000', 'none', 'center'),
            ('вручается', -86, -32, font, 44, '#000000', 'none', 'left'),
            ('Имя Фамилия', -86, 41, font, 30, '#000000', 'none', 'right'),
            ('Год', -151, 241, font, 14, '#000000', 'none', 'left'),
            ('Подпись', 107, 241, font, 14, '#000000', 'none', 'left'),
        )
        texts_horizontal = (
            ('Грамота', -180, -214, font, 94, '#000000', 'none', 'center'),
            ('вручается', -95, -90, font, 44, '#000000', 'none', 'left'),
            ('Имя Фамилия', -86, -17, font, 30, '#000000', 'none', 'right'),
            ('Год', -159, 196, font, 14, '#000000', 'none', 'left'),
            ('Подпись', 122, 196, font, 14, '#000000', 'none', 'left'),
        )
        headers = ('text', 'coordinate_x', 'coordinate_y', 'font',
                   'font_size', 'font_color', 'text_decoration', 'align')
        format = {
            True: texts_horizontal,
            False: texts_vertical
        }
        user = User.objects.get(id=1)
        for i in range(10):
            document, created = Document.objects.get_or_create(
                title=f'Шаблон {i+1}',
                user=user,
                background=f'backgrounds/template0{i}.jpg',
                thumbnail=f'thumbnails/template0{i}.jpg'
            )
            if document.background.width > document.background.height:
                document.is_horizontal = True
                document.save()
            TextField.objects.bulk_create(
                TextField(document=document,
                          **dict(zip(headers, t)))
                for t in format[document.is_horizontal]
            )
