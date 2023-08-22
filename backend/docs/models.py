from django.conf import settings
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from users.models import User


CATEGORY_CHOICES = (
    ('diplomas', 'Дипломы'),
    ('certificates', 'Сертификаты'),
    ('appreciations', 'Благодарности'),
    ('awards', 'Грамоты'),
    ('others', 'Другое'),
)


class Document(models.Model):
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название документа',
        validators=[
            MinLengthValidator(6, message='Введите слово больше 6 символов')
        ],
        help_text='Введите название документа',
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(
        'Category',
        max_length=15,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    preview = models.CharField(
        max_length=255,
        verbose_name='Превью',
    )
    background_image = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Фон',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title


class Field(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Текст поля')
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')
    font = models.CharField(
        max_length=50,
        verbose_name='Название шрифта',
        help_text='Введите название шрифта'
    )
    font_size = models.PositiveSmallIntegerField(
        default=14,
        validators=[
            MinValueValidator(8, message='Введите число начиная от 8')
        ],
        verbose_name='Размер шрифта',
        help_text='Введите размер шрифта'
    )
    font_color = models.CharField(max_length=100, verbose_name='Цвет шрифта')

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return self.document_id


class Stamp(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(verbose_name='Размер элемента')
    stamp_image = models.CharField(
        max_length=255,
        verbose_name='Изображение элемента',
    )
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')

    class Meta:
        ordering = ('document_id',)
        verbose_name = 'Штамп'
        verbose_name_plural = 'Штампы'

    def __str__(self):
        return self.document_id


class Category(models.Model):
    name = models.CharField(
        max_length=55,
        db_index=True,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
        help_text='Введите категорию документа'
    )
    slug = models.SlugField(
        max_length=55,
        blank=True,
        unique=True,
        verbose_name='Уникальный префикс',
        help_text='Введите уникальный префикс'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
