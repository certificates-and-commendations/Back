import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='John Doe',
        email='john_doe@email.com',
        password='12345678'
    )


@pytest.fixture
def user_token(user):
    return Token.objects.create(user=user)
