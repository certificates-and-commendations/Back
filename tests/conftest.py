import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from docs.models import Category, Document, Field, Stamp


@pytest.fixture
def client():
    client=APIClient()
    return client

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='john_doe@email.com',
        password='12345678'
    )

@pytest.fixture
def user_token(user):
    return Token.objects.create(user=user)

@pytest.fixture
def category():
    return Category.objects.create(
        name='diplomas',
        slug='diplomas'
    )


@pytest.fixture
def document(category, user):
    return Document.objects.create(
        title='Test Document',
        user_id=user,
        category_id=category,
        preview='Test Preview',
        background_image='Test Background Image'
    )


@pytest.fixture
def field(document):
    return Field.objects.create(
        document_id=document,
        text='Test Text',
        coordinate_y=100,
        coordinate_x=200,
        font='Arial',
        font_size=12,
        font_color='black'
    )


@pytest.fixture
def stamp(document):
    return Stamp.objects.create(
        document_id=document,
        size=50,
        stamp_image='Test Stamp Image',
        coordinate_y=150,
        coordinate_x=250
    )
