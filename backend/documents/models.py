from django.core.validators import (FileExtensionValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User

FONT_DECORATIONS = (
    ('underline', 'подчеркнутый'),
    ('strikethrough', 'зачеркнутый'),
    ('none', 'обычный')
)

TEXT_ALIGN = (
    ('left', 'по левому краю'),
    ('right', 'по правому краю'),
    ('center', 'по центру')
)


class Document(models.Model):
    """
    Модель представляющая Документ.
    """
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название документа',
        help_text='Введите название документа',
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        verbose_name='Превью',
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category',
        max_length=15,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    color = models.ManyToManyField(
        'TemplateColor',
        related_name='colors',
    )
    background = models.ImageField(
        'BackgroundImage',
        upload_to='backgrounds/',
        blank=True
    )
    is_horizontal = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title


class TextField(models.Model):
    """
    Модель представляет поля документа.
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name='Текст поля')
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')

    font = models.ForeignKey(
        'Font',
        related_name='text',
        max_length=50,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
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
    font_color = models.CharField(
        max_length=7,
        verbose_name='Цвет шрифта'
    )
    text_decoration = models.CharField(
        max_length=20,
        choices=FONT_DECORATIONS,
        default='none',
        verbose_name='Подчёркивание шрифта'
    )
    align = models.CharField(
        max_length=6,
        choices=TEXT_ALIGN,
        default='left')

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return f'поля текста для документа {self.document.title}'


class Category(models.Model):
    """
    Модель представляет категории.
    """
    name_validator = RegexValidator(
        regex=r'^[А-Яа-я]+$',
        message='Название должно содержать буквы кириллицы',
        code='invalid_name'
    )

    name = models.CharField(
        max_length=55,
        db_index=True,
        validators=[name_validator],
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


class TemplateColor(models.Model):
    """
    Модель представляет цвета фона шаблона.
    """
    hex = models.CharField(
        max_length=7,
        verbose_name='Цвет фона',
        help_text='Введите цвет фона'
    )
    slug = models.SlugField(
        max_length=55,
        blank=True,
        unique=True,
        verbose_name='Уникальный префикс',
        help_text='Введите уникальный префикс'
    )

    class Meta:
        verbose_name = 'Цвет фона'
        verbose_name_plural = 'Цвета фона'

    def __str__(self):
        return self.slug


class Element(models.Model):
    """
    Модель для изображения штампа, подписи, т.д.
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')
    image = models.ImageField(
        upload_to='elements/',
        blank=True,
    )

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    # админка не принимает рк, сделала так
    def __str__(self):
        # return self.pk
        return f'элемент для документа {self.document.title}'


class Favourite(models.Model):
    """
    Модель для избранных шаблонов
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favourite',
                             verbose_name='Пользователь',)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,
                                 related_name='favourite',
                                 verbose_name='Шаблон в избранном',)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'document'], name='unique_favorite'
            )
        ]


class Font(models.Model):
    """Модель для шрифтов."""
    font = models.CharField(max_length=100)
    is_bold = models.BooleanField()
    is_italic = models.BooleanField()
    font_file = models.FileField(
        upload_to='fonts/',
        validators=[FileExtensionValidator(allowed_extensions=['ttf'])])

    class Meta:
        verbose_name = 'Шрифт'
        verbose_name_plural = 'Шрифты'

    def __str__(self):
        return self.font
