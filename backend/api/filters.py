import django_filters
from documents.models import Document


class DocumentFilter(django_filters.FilterSet):
    """Фильтр документов по расположению/категории"""
    is_horizontal = django_filters.BooleanFilter()
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')

    class Meta:
        model = Document
        fields = ['is_horizontal', 'category', ]
