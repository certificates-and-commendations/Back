from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        'Почта',
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField('Имя', max_length=150, blank=False)

    last_name = models.CharField(('Фамилия'), max_length=150, blank=False)

    avatar_image = models.ImageField(  # возможно нужна валидация здесь или на фронте касательно размера изображения
        verbose_name='Фото',
        upload_to='users/',
        default='users/avatar_image.jpg',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username', )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return (f'{self.username}: {self.first_name}'
                f'{self.last_name}, {self.email}')
