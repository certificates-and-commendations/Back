from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from users.models import User

CATEGORY_CHOICES = (
    ('diplomas', 'Дипломы'),
    ('certificates', 'Сертификаты'),
    ('appreciations', 'Благодарности'),
    ('awards', 'Грамоты'),
)


class Document(models.Model):
    """
    Модель представляющая Документ.
    """
    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название документа',
        validators=[
            MinLengthValidator(6, message='Введите слово больше 6 символов')
        ],
        help_text='Введите название документа',
    )
    thumbnail = models.CharField(
        max_length=255,
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
    is_completed = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category',
        max_length=15,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    color = models.ForeignKey(
        'TemplateColor',
        on_delete=models.SET_NULL,
        null=True
    )
    textFields = models.ManyToManyField('TextField')
    images = models.ManyToManyField(
        'Image',
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


class TextField(models.Model):
    """
    Модель представляет поля документа.
    """
    text = models.CharField(max_length=255, verbose_name='Текст поля')
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')
    fonts = models.ManyToManyField(
        'Font',
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
    font_color = models.CharField(
        max_length=7,
        verbose_name='Цвет шрифта'
    )
    text_decoration = models.CharField(
        max_length=20,
        verbose_name='Подчёркивание шрифта'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

    def __str__(self):
        return self.pk


class Category(models.Model):
    """
    Модель представляет категории.
    """
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
        ordering = ('-id',)
        verbose_name = 'Цвет фона'
        verbose_name_plural = 'Цвета фона'

    def __str__(self):
        return self.pk


class Font(models.Model):
    """
    Модель представляет шрифт полей документа.
    """
    font_family = models.CharField(
        max_length=55,
        verbose_name='Название шрифта'
    )
    font_style = models.CharField(
        max_length=55,
        verbose_name='Начертание шрифта'
    )
    font_weight = models.CharField(
        max_length=55,
        verbose_name='Насыщенность шрифта'
    )
    url = models.CharField(max_length=55)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Шрифт'
        verbose_name_plural = 'Шрифты'
        unique_together = ('font_style', 'font_weight')

    def __str__(self):
        return self.pk


class Image(models.Model):
    """
    Модель для изображения штампа, фона, подписи.
    """
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')
    url = models.CharField(max_length=255)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'

    def __str__(self):
        return self.pk
