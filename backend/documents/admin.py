from django.contrib import admin

from .models import (Category, Document, Element, Favourite, TemplateColor,
                     TextField)

# from PIL import Image, ImageDraw


class FavouriteInline(admin.TabularInline):
    model = Favourite
    min_num = 1
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    inlines = (FavouriteInline,)
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
    readonly_fields = ['thumbnail']

    # def thumbnail(self, obj):
    #     if not obj.thumbnail:
    #         image = Image.open(obj.background) # этот код не дописан еще

    #         return
    #     return obj.thumbnail


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
        'is_bold',
        'is_italic',
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
    list_filter = ('name', 'slug', )
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
    search_fields = ('image', 'document__id', )


admin.site.register(Element, ElementAdmin)
