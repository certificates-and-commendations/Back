import pytest
from django.core.exceptions import ValidationError
from users.models import User
from docs.models import Category, Document, Field, Stamp


pytestmark = pytest.mark.django_db


class TestDocsModels:
    def test_document_category_relation(self):
        Document.objects.create(
            title='Document 1',
            user_id=User.objects.create(username='test_1', email='test@test1.ru'),
            category_id=Category.objects.create(
                id=0,
                name='diplomas',
                slug='diplomas'
            )
        )
        Document.objects.create(
            title='Document 2',
            user_id=User.objects.create(username='test_2', email='test@test2.ru'),
            category_id=Category.objects.create(
                id=1,
                name='certificates',
                slug='certificates'
            )
        )

        assert Document.objects.count() == 2

        certificates = Document.objects.filter(category_id=1)
        diplomas = Category.objects.filter(name='diplomas')
        assert certificates.first().title == 'Document 2'
        assert diplomas.first().slug == 'diplomas'

    def test_document_field_relation(self, document, field):
        assert field.document_id == document
        assert document.field_set.count() == 1
        assert document.field_set.first().text == 'Test Text'
        assert field.document_id.title == 'Test Document'
        assert document.category_id.name == 'diplomas'

    def test_document_title_min_length(self, category):
        doc = Document(
            title='Short',
            user_id=User.objects.create(username='testuser', email='length@test.com'),
            category_id=category,
            preview='Test Preview',
            background_image='Test Background Image'
        )

        with pytest.raises(ValidationError) as e:
            doc.full_clean()

        assert 'title' in e.value.error_dict
        assert 'Введите слово больше 6 символов' in str(e.value)

    def test_document_save(self, document):
        document.save()
        assert Document.objects.filter(pk=document.pk).exists()

    def test_stamp_lookups(self, stamp):
        assert Stamp.objects.get(size=50) == stamp
