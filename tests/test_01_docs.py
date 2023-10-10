import pytest
from django.core.exceptions import ValidationError
from documents.models import Category, Document, Element, Favourite, TextField

pytestmark = pytest.mark.django_db


class TestDocumentsModels:
    def test_document_category_relation(self, user):
        Document.objects.create(
            title='Document 1',
            user=user,
            category=Category.objects.create(
                id=0,
                name='diplomas',
                slug='diplomas'
            )
        )
        Document.objects.create(
            title='Document 2',
            user=user,
            category=Category.objects.create(
                id=1,
                name='certificates',
                slug='certificates'
            )
        )

        assert Document.objects.count() == 2

        certificates = Document.objects.filter(category=1)
        diplomas = Category.objects.filter(name='diplomas')
        assert certificates.first().title == 'Document 2'
        assert diplomas.first().slug == 'diplomas'

    def test_document_field_relation(self, document, text_field):
        assert text_field.document.id == document.id
        assert document.textfield_set.count() == 1
        assert document.textfield_set.first().text == 'Test Text'
        assert text_field.document.title == 'Test Document'
        assert document.category.name == 'diplomas'

    def test_text_field_font_size_min_value(self):
        field = TextField(font_size=7)

        with pytest.raises(ValidationError) as e:
            field.full_clean()

        assert 'font_size' in e.value.error_dict
        assert 'Введите число начиная от 8' in str(e.value)

    def test_category_invalid_name_latin_char(self):
        with pytest.raises(ValidationError) as e:
            Category(name='Test123').full_clean()

        assert 'name' in e.value.error_dict
        assert 'Название должно содержать буквы кириллицы' in str(e.value)

    def test_category_invalid_name_with_space_char(self):
        with pytest.raises(ValidationError) as e:
            Category(name='Test Category').full_clean()

        assert 'name' in e.value.error_dict
        assert 'Название должно содержать буквы кириллицы' in str(e.value)

    def test_category_valid_name(self):
        try:
            Category(name='ТестоваяКатегория').full_clean()
        except ValidationError:
            pytest.fail('Category name validation failed for valid name')

    def test_document_save(self, document):
        document.save()
        assert Document.objects.filter(id=document.id).exists()

    def test_element_lookups(self, element):
        assert Element.objects.get(image='elements/') == element

    def test_document_creation(self, document, user):
        assert document.title == 'Test Document'
        assert document.user.email == user.email
        assert document.category.name == 'diplomas'

    def test_text_field_creation(self, text_field, font):
        assert text_field.text == 'Test Text'
        assert text_field.font == font

    def test_category_creation(self, category):
        assert category.name == 'diplomas'
        assert category.slug == 'diplomas'

    def test_font_creation(self, font):
        assert font.font == 'Arial'
        assert font.is_bold
        assert not font.is_italic
        assert font.font_file == 'fonts/Arial.ttf'

    def test_element_creation(self, element):
        assert element.coordinate_y == 20
        assert element.image == 'elements/'

    def test_category_str(self, category):
        assert str(category) == category.name

    def test_text_field_str(self, text_field):
        expected = f'поля текста для документа {text_field.document.title}'
        assert str(text_field) == expected

    def test_element_str(self, element):
        expected = f'элемент для документа {element.document.title}'
        assert str(element) == expected

    def test_add_and_remove_documents_from_favorites(self, document, user):
        document1 = Document.objects.create(title='Document 1', user=user)
        document2 = Document.objects.create(title='Document 2', user=user)

        Favourite.objects.create(user=user, document=document1)
        favourite2 = Favourite.objects.create(user=user, document=document2)

        assert Favourite.objects.filter(user=user).count() == 2

        favourite2.delete()

        assert Favourite.objects.filter(user=user).count() == 1
        assert not Favourite.objects.filter(
            user=user, document=document2
        ).exists()
