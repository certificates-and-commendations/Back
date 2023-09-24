import pytest

pytestmark = pytest.mark.django_db

URL_DOCS = '/api/documents/'
DOC_FIELDS = ('id', 'title', 'thumbnail', 'category', 'color', 'is_horizontal')


def test_get_documents(client, document, document_horizontal):
    response = client.get(f'{URL_DOCS}')
    assert response.status_code == 200, (
        'Не удалось получить список шаблонов')
    data = response.json()
    for field in DOC_FIELDS:
        assert field in data['results'][0], (
            f'GET-запрос к {URL_DOCS} должен вернуть поле {field}')


@pytest.mark.parametrize('filter_name, filters, expected_result', [
    ('is_horizontal', 'is_horizontal=false', 1),
    ('category', 'category=diplomas&category=certificates', 2),
    ('category&is_horizontal', 'category=diplomas&is_horizontal=true', 0),
])
def test_get_documents_with_filters(client, filters, expected_result,
                                    document, document_horizontal,
                                    filter_name):
    response = client.get(f'{URL_DOCS}?{filters}')
    assert response.status_code == 200, (
        'Не удалось получить список шаблонов c фильтром is_horizontal=false')
    assert response.json()['count'] == expected_result, (
        f'Для GET-запрос к {URL_DOCS} должена работать фильтрация по полю '
        f'{filter_name}')
