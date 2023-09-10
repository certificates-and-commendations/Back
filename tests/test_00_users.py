import pytest
from users.models import User

pytestmark = pytest.mark.django_db

URL_USERS = '/api/users/'
URL_TOKEN = '/api/auth/token/'
USER_FIELDS = ('email', 'id')


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

    response = client.post(URL_USERS, new_user, format='json')
    assert response.status_code == 400, (
        'Нельзя зарегистрироваться на одну почту дважды')


def test_user_profile(client, user, user_token):
    response = client.get(f'{URL_USERS}{user.id}/')
    assert response.status_code == 401, (
        'Нелязя получить доступ к профилю без авторизации')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response_with_creds = client.get(f'{URL_USERS}{user.id}/')
    assert response_with_creds.status_code==200, (
        'Авторизованный пользователь не может получить доступ к своему профилю'
    )
    for field in USER_FIELDS:
        assert getattr(user, field) == response_with_creds.json().get(field), (
            f'В ответе на GET {URL_USERS}{user.id}/ нет поля {field}')



def test_user_me(client, user_token):
    response = client.get(f'{URL_USERS}me/')
    assert response.status_code == 401
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.get(f'{URL_USERS}me/')
    assert response.status_code == 200
    for field in USER_FIELDS:
        assert field in response.json(), (f'GET-запрос не вернул поля {field}')


def test_change_password(client, user_token):
    good_params = {
        'new_password': 'Test_user1#',
        'current_password': '12345678',
    }
    bad_params = {
        'new_pass': 'Test_user1#',
        'current_password': '12345678',
    }
    response = client.post(f'{URL_USERS}set_password/')
    assert response.status_code == 401, (
        'Неавторизованный пользователь не может поменять пароль')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.post(f'{URL_USERS}set_password/',
                           bad_params, format='json')
    assert response.status_code == 400, (
        f'Некорретные данные при обращение к {URL_USERS}set_password/ должны '
        f'вернуть ошибку 400')
    response = client.post(f'{URL_USERS}set_password/', good_params,
                           format='json')
    assert response.status_code == 204, (
        'Не удалось поменять пароль пользователя')


def get_user_login(client):
    params = {
        'password': 'Test_user1',
        'email': 'johndoe@email.com',
    }
    response = client.post(f'{URL_TOKEN}login/', params, format='json')
    assert response.status_code == 201, (
        'Не удалось получить токен авторизации')
    assert 'auth_token' in response.json(), (
        'Токена авторизации нет в ответе')


def get_user_logout(client, user_token):
    response = client.post(f'{URL_TOKEN}logout/')
    assert response.status_code == 401, (
        'Неавторизованный пользователь не может удалить токен')
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    response = client.post(f'{URL_TOKEN}logout/')
    assert response.status_code == 204, (
        'Не удалось удалить токен авторизованного пользователя')
