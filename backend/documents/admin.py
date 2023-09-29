from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Category, Document, Element,
                     Font, Favourite, TemplateColor,
                     TextField)
from api.utils import create_thumbnail


class FavouriteInline(admin.TabularInline):
    model = Favourite
    min_num = 0
    extra = 0


class TextFieldInline(admin.TabularInline):
    model = TextField
    min_num = 0
    extra = 0


class ElementInline(admin.TabularInline):
    model = Element
    readonly_fields = ['mini_image']

    def mini_image(self, obj):
        if not (obj.pk and obj.image):
            return 'Элемент не добавлен'
        return mark_safe(f'<img src="{obj.image.url}"'
                         f'style="max-height: 40px;">')
    min_num = 0
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    inlines = (FavouriteInline, TextFieldInline, ElementInline, )
    list_display = (
        'id',
        'title',
        'thumbnail',
        'time_create',
        'time_update',
        'user',
        'category',
        'background',
        'color',
        'is_horizontal',
    )
    list_filter = ('category', 'is_horizontal', )
    search_fields = ('title', 'user__email', )
    ordering = ('time_create', )
    readonly_fields = ('thumbnail',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        thumbnail = create_thumbnail(obj)
        obj.save()
        return thumbnail


admin.site.register(Document, DocumentAdmin)


class TextFieldAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'document',
        'text',
        'coordinate_x',
        'coordinate_y',
        'font',
        'font_size',
        'font_color',
        'text_decoration',
        'align',
    )
    search_fields = ('id', 'document__id',)


admin.site.register(TextField, TextFieldAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'slug',
    )
    list_filter = ('name', )
    search_fields = ('name', 'slug', )


admin.site.register(Category, CategoryAdmin)


class TemplateColorAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'hex',
        'slug',
    )
    list_filter = ('slug', )
    search_fields = ('id', 'slug', )


admin.site.register(TemplateColor, TemplateColorAdmin)


class ElementAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'document',
        'coordinate_x',
        'coordinate_y',
        'image',
    )
    list_filter = ('document', )
    search_fields = ('document__id', )


admin.site.register(Element, ElementAdmin)


class FontAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'font',
        'is_bold',
        'is_italic',
        'font_file',
    )
    list_filter = ('font', )
    search_fields = ('font', )


admin.site.register(Font, FontAdmin)
