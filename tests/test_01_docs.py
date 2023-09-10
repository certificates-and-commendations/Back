import pytest
from django.core.exceptions import ValidationError
from users.models import User
from documents.models import Category, Document, Element, TextField


pytestmark = pytest.mark.django_db


class TestDocsModels:
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
        assert text_field.id == document.text_fields
        assert document.field_set.count() == 1
        assert document.field_set.first().text == 'Test Text'
        assert text_field.id.title == 'Test Document'
        assert document.category.name == 'diplomas'

    def test_document_title_min_length(self, category, document, image):
        doc = Document(
            title='Short',
            user=User.objects.create(email='length@test.com'),
            category=category,
            thumbnail='Test Preview',
            images=document.image.set([50, 55, '/'])
        )

        with pytest.raises(ValidationError) as e:
            doc.full_clean()

        assert 'title' in e.value.error_dict
        assert 'Введите слово больше 6 символов' in str(e.value)

    def test_document_save(self, document):
        document.save()
        assert Document.objects.filter(pk=document.pk).exists()

    def test_stamp_lookups(self, image):
        assert Image.objects.get(url='/') == image

    def test_document_creation(self, document):
        assert document.title == 'Test Document'
        assert document.user.username == 'testuser'
        assert document.category.name == 'test category'

    def test_text_field_creation(self, text_field):
        assert text_field.text == 'test text'
        assert text_field.fonts.first().font_family == 'Arial'

    def test_category_creation(self, category):
        assert category.name == 'diplomas'
        assert category.slug == 'diplomas'

    def test_font_creation(self, font):
        assert font.font_family == 'Cosmic'
        assert font.url == '/'

    def test_image_creation(self, image):
        assert image.coordinate_y == 150
        assert image.url == '/'
