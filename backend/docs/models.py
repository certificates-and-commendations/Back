from django.core.validators import MinLengthValidator
from django.db import models

from users.models import User


class Document(models.Model):
    CATEGORY_CHOICES = (
        ('diplomas', 'Дипломы'),
        ('certificates', 'Сертификаты'),
        ('appreciations', 'Благодарности'),
        ('awards', 'Грамоты'),
        ('others', 'Другое'),
    )

    title = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Название документа',
        validators=[MinLengthValidator(6)],
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория',
    )
    preview = models.CharField(
        max_length=255,
        verbose_name='Превью',
    )
    background_image = models.CharField(
        max_length=255,
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
    text = models.CharField(max_length=255)
    coordinate_y = models.IntegerField(verbose_name='Координата Y')
    coordinate_x = models.IntegerField(verbose_name='Координата X')
    font = models.CharField(verbose_name='Название шрифта', max_length=100)
    font_size = models.IntegerField(verbose_name='Размер шрифта')
    font_color = models.CharField(verbose_name='Цвет шрифта', max_length=100)

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class Stamp(models.Model):
    document_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    size = models.IntegerField(verbose_name='Размер элемента')
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
