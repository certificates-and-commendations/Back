import pytest

pytestmark = pytest.mark.django_db


def test_get_and_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200, ('Не удалось получить список пользователей')

def test_post_user(client):
    new_user = {
        'email': 'newuser@email.com',
        'password': '12345678',
    }
    response = client.post('/api/users', new_user, format='json')
    assert response.status_code == 201, ('Не удалось создать пользователя')
    
    response = client.post('/api/users', new_user, format='json')
    assert response.status_code == 400, ('Нельзя зарегистрироваться на одну почту дважды')
    
def test_user_profile(client, user):
    response = client.get(f'/api/users/{user.id}/')
    assert response.status_code ==200, ('Не удалось получить профиль пользователя')