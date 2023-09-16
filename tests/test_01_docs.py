import pytest
from django.core.exceptions import ValidationError
from documents.models import Category, Document, Element, TextField
from users.models import User

pytestmark = pytest.mark.django_db


class TestDocumentsModels:
    def test_document_category_relation(self):
        Document.objects.create(
            title='Document 1',
            user=User.objects.create(email='test@test1.ru'),
            category=Category.objects.create(
                id=0,
                name='diplomas',
                slug='diplomas'
            )
        )
        Document.objects.create(
            title='Document 2',
            user=User.objects.create(email='test@test2.ru'),
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

    def test_text_field_font_size_min_value(self, document):
        field = TextField(font_size=7)

        with pytest.raises(ValidationError) as e:
            field.full_clean()

        assert 'font_size' in e.value.error_dict
        assert 'Введите число начиная от 8' in str(e.value)

    def test_document_save(self, document):
        document.save()
        assert Document.objects.filter(id=document.id).exists()

    def test_element_lookups(self, element):
        assert Element.objects.get(image='elements/') == element

    def test_document_creation(self, document, user):
        assert document.title == 'Test Document'
        assert document.user.email == 'john_doe@email.com'
        assert document.category.name == 'diplomas'

    def test_text_field_creation(self, text_field):
        assert text_field.text == 'Test Text'
        assert text_field.font == 'Arial'

    def test_category_creation(self, category):
        assert category.name == 'diplomas'
        assert category.slug == 'diplomas'

    def test_font_creation(self, font):
        assert font.font == 'Arial'
        assert font.is_bold
        assert not font.is_italic
        assert font.font_file == 'arial.ttf'

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
