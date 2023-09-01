import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from documents.models import Category, Document, Element, TextField


@pytest.fixture
def client():
    client = APIClient()
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
def document(category, image, user, text_field):
    return Document.objects.create(
        title='Test Document',
        user=user,
        category=category,
        thumbnail='Test Preview',
        text_fields=text_field,
        images=image,
    )


@pytest.fixture
def text_field():
    return TextField.objects.create(
        text='Test Text',
        coordinate_y=100,
        coordinate_x=200,
        font='font',
        font_color='#000000',
        text_decoration='underline'
    )


@pytest.fixture
def image():
    return Element.objects.create(
        coordinate_y=150,
        coordinate_x=250,
        url='/'
    )
