import pytest
from users.models import User

pytestmark = pytest.mark.django_db

URL_USERS = '/api/users/'
URL_TOKEN = '/api/auth/token/'
USER_FIELDS = ('email', 'id')
PROFILE_FIELDS = ('favourites', 'documents')


def test_get_users(client):
    response = client.get(URL_USERS)
    assert response.status_code == 200, (
        'Не удалось получить список пользователей')


def test_post_user(client):
    new_user = {
        'email': 'newuser@email.com',
        'password': 'Test123$',
    }
    response = client.post(URL_USERS, new_user, format='json')
    assert response.status_code == 201, (
        'Не удалось создать пользователя')
    user = User.objects.filter(email=new_user['email'])
    assert user.count() == 1, ('Пользователь не создан')
    for field in USER_FIELDS:
        assert getattr(user[0], field) == response.json().get(field), (
            f'POST-запрос не вернул поля {field}')
    bad_data = {
        'email': 'test@somemail.com',
        'username': 'test_user',
    }
    response = client.post(URL_USERS, new_user, format='json')
    assert response.status_code == 400, (
        'Нельзя зарегистрироваться дважды')
    response = client.post(URL_USERS, bad_data, format='json')
    assert response.status_code == 400, (
        f'Некорретные данные при обращение к {URL_USERS} должны'
        f' вернуть ошибку 400')


def test_user_profile(client, user, user_token):
    response = client.get(f'{URL_USERS}{user.id}/')
    assert response.status_code == 401, (
        'Нелязя получить доступ к профилю без авторизации')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response_with_creds = client.get(f'{URL_USERS}{user.id}/')
    assert response_with_creds.status_code == 200, (
        'Авторизованный пользователь не может получить доступ к своему профилю'
    )
    for field in PROFILE_FIELDS:
        assert field in response.json(), (
            f'В профиле пользователя нет {field}')


def test_user_me(client, user_token):
    response = client.get(f'{URL_USERS}me/')
    assert response.status_code == 401
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.get(f'{URL_USERS}me/')
    assert response.status_code == 200
    for field in PROFILE_FIELDS:
        assert field in response.json(), (
            f'В профиле пользователя нет {field}')


def test_user_login(client, user):
    params = {
        'password': '12345678',
        'email': user.email,
    }
    response = client.post(f'{URL_TOKEN}login/', params, format='json')
    assert response.status_code == 200, (
        'Не удалось получить токен авторизации')
    assert 'auth_token' in response.json(), (
        'Токена авторизации нет в ответе')


def test_user_logout(client, user_token):
    response = client.post(f'{URL_TOKEN}logout/')
    assert response.status_code == 401, (
        'Неавторизованный пользователь не может удалить токен')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.post(f'{URL_TOKEN}logout/')
    assert response.status_code == 204, (
        'Не удалось удалить токен авторизованного пользователя')


def test_user_regist(client, mocker):
    mocker.patch(
        'api.views.gmail_send_message'
    )
    valid_user = {
        'email': 'mail0@mail.com',
        'password': 'Passw0rd!'
    }
    response = client.post('/api/auth/regist/', valid_user, format='json')
    assert response.status_code == 200, ('Не удалось зарегистрировать '
                                         'пользователя')
    not_valid_user = {
        'email': 'mail0@mail.com',
        'password': '1'
    }
    response = client.post('/api/auth/regist/', not_valid_user, format='json')
    assert response.status_code == 400, ('Удалось зарегистрировать '
                                         'пользователя с простым паролем')


def test_regist_confirm(client, user):
    data = {
        'code': user.code,
        'email': user.email
    }
    response = client.post('/api/auth/confirm/', data, format='json')
    assert response.status_code == 200, ('Не удалось подтвердить почту')
    assert 'Token' in response.json(), ('После успешного подтверждения почты '
                                        'не получен токен')


def test_user_delete(client, user, user_token):
    data = {
        'current_password': '12345678',
        }
    response = client.delete(f'{URL_USERS}{user.id}/', data, format='json')
    assert response.status_code == 401, (
        'Неавторизированному пользователю удалось удалить профиль')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.delete(f'{URL_USERS}{user.id}/', data, format='json')
    assert response.status_code == 204, (
        'Авторизированному пользователю не удалось удалить свой профиль')
