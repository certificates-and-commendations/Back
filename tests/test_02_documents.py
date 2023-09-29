import pytest
from django.conf import settings

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


def test_documents_post(client, mocker, font, user, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    mocker.patch(
        'api.serializers.certificate_serializers.create_thumbnail'
    )
    doc = {
        'title': 'test template',
        'background': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKAP/2Q==',
        'is_horizontal': False,
        'texts': [
            {
                'text': 'Грамота',
                'coordinate_x': -174,
                'coordinate_y': -146,
                'font': {
                    'font': 'Arial',
                    'is_bold': True,
                    'is_italic': False
                },
                'font_size': 94,
                'font_color': '#000000',
                'text_decoration': 'underline',
                'align': 'center'
            }
        ],
        'elements': [
            {
                'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXY/j///9/AAn7A/0FQ0XKAAAAAElFTkSuQmCC',
                'coordinate_x': -300,
                'coordinate_y': 200
            }
        ]
    }
    response = client.post(f'{URL_DOCS}', doc, format='json')
    assert response.status_code == 201
    for field in DOC_FIELDS:
        assert field in response.json(), (
            f'POST-запрос к {URL_DOCS} должен вернуть поле {field}')


def test_documents_detail(client, document):
    response = client.get(f'{URL_DOCS}{document.id}/')
    assert response.status_code == 200, (
        f'GET-запрос к {URL_DOCS}{document.id}// должен вернуть ответ 200')
    doc_fields = ('id', 'user', 'title', 'background', 'category', 'color',
                  'is_horizontal', 'texts', 'elements')
    data = response.json()
    for field in doc_fields:
        assert field in data, (
            f'GET-запрос к {URL_DOCS}{document.id}// должен вернуть поле'
            f' {field}')
