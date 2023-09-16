import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from documents.models import (Category, Document, Element, Font,
                              TemplateColor, TextField)


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
def document(category, user):
    return Document.objects.create(
        title='Test Document',
        user=user,
        category=category,
        thumbnail='media/',
        # text_fields=text_field,
        background='backgrounds/',
    )


@pytest.fixture
def text_field(document):
    return TextField.objects.create(
        document=document,
        text='Test Text',
        coordinate_y=10,
        coordinate_x=10,
        font='Arial',
        font_size=12,
        font_color='#000000',
        is_bold=False,
        is_italic=False,
        text_decoration='none',
        align='left'
    )


@pytest.fixture
def template_color():
    return TemplateColor.objects.create(
        hex='#FF0000',
        slug='test-color'
    )


@pytest.fixture
def element(document):
    return Element.objects.create(
        document=document,
        coordinate_y=20,
        coordinate_x=20,
        image='elements/'
    )


@pytest.fixture
def font():
    return Font.objects.create(
        font='Arial',
        is_bold=True,
        is_italic=False,
        font_file='arial.ttf'
    )
