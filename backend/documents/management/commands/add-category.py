from django.core.management import BaseCommand
from documents.models import Category
from data.category import CATEGORY_CHOICES


class Command(BaseCommand):
    help = 'Загрузка категорий'

    def add_category(self, parser):
        parser.add_argument(nargs='?', type=str)

    def handle(self, *args, **options):

        for choice in CATEGORY_CHOICES:
            Category.objects.create(name=choice[1],
                                    slug=choice[0])

        self.stdout.write(self.style.SUCCESS('Все категории загружены!'))
