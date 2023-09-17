from django.core.management.base import BaseCommand, CommandError
from documents.models import Font


class Command(BaseCommand):

    def handle(self, *args, **options):
        headers = ['font', 'is_bold', 'is_italic', 'font_file']
        fonts = (
            ('Arial', False, False, 'fonts/Arial.ttf'),
            ('Arial', True, False, 'fonts/Arial Bold.ttf'),
            ('Arial', False, False, 'fonts/Arial Italic.ttf'),
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
        )
        for font in fonts:
            f = dict(zip(headers, font))
            Font.objects.create(**f)
