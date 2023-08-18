from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'avatar_image',
        'avatar',
    )
    list_filter = ('first_name', 'last_name',)
    search_fields = ('email', 'username', 'first_name',
                     'last_name', )
    ordering = ('email',)
    readonly_fields = ["avatar"]

    def avatar(self, obj):
        if not (obj.pk and obj.avatar_image):
            return 'Добавьте фото'
        return mark_safe(f'<img src="{obj.avatar_image.url}"'
                         f'style="max-height: 40px;">')

    avatar.short_description = 'Изображение'


admin.site.register(User, CustomUserAdmin)
