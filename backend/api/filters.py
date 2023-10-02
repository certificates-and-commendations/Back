from django import forms
import django_filters
from documents.models import Category, Document


class DocumentFilter(django_filters.FilterSet):
    """Фильтр документов по расположению/категории"""

    is_horizontal = django_filters.BooleanFilter()
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Document
        fields = ['is_horizontal', 'category', ]
