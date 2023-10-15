<a id="anchor"></a>
# Приложение "Генератор грамот" 

![example workflow](https://github.com/certificates-and-commendations/Back/actions/workflows/certificates_deploy.yml/badge.svg)

## Описание

Проект выпускников _Яндекс.Практикум_ 

Благодаря этому проекту можно создавать грамоты, дипломы, благодарности и сертификаты. Наш онлайн-редактор позволяет создавать документы на основе предустановленных шаблонов, а также дает возможность загружать собственные фоны для будущих грамот, дипломов и т.д. 

Широкий набор средств редактирования включает:
- добавление неограниченного количества текстовых полей;
- выбор шрифта, размера, цвета, стилей для шрифта;
- замена фона документа на любом этапе редактирования;

Пользователям доступна возможность загружать собственные шрифты или использовать предустановленные. Также реализована функция добавления изображения печатей, штампов, подписей, факсимиле в формате PNG. 

Кроме того, пользователю доступна функция по созданию сразу нескольких одинаковых документов  для разных получателей (автогенерация нескольких документов с разными ФИО). 

В Личном кабинете пользователя отражается информация о всех документах, которые он когда-либо редактировал, а также список с избранными документами. 

Для доступа к основному функционалу требуется пройти бесплатную регистрацию. Реализована функция подтверждения почты пользователя и восстановления пароля. 


### Технологии

Python 3.9.10

Django 3.2

djangorestframework 3.14.0

### Инфраструктура: 
* Docker
* NGINX
* GUNICORN
* база даннных POSTGRESQL

### Основные библиотеки:

- аутентификация Djoser
- документация drf-yasg
- инструменты Google Api для подстверждения аутентификации пользователей
- работа с изображениями Pillow
- генерация PDF reportlab
- автоопределение доминантных цветов шаблона на основе методов sklearn.cluster (KMeans и KDTree)
- codecs для парсинга CSV 

### Запуск проекта
~~~
склонировать проект git clone https://github.com/certificates-and-commendations/Back
~~~
- При первом запуске для функционирования проекта обязательно установить виртуальное окружение, установить зависимости,  выполнить миграции:

```
python -m venv venv

source venv/Scripts/activate

python -m pip install --upgrade pip
```
- Установите зависимости из файла requirements.txt

```
pip install -r requirements.txt
```
- Выполните миграции БД. Из папки backend с файлом manage.py выполните команду:
```
python manage.py makemigrations
python manage.py migrate
```
- Для создания суперюзера из папки backend с файлом manage.py выполните команду:
```
python manage.py createsuperuser
```

- Для загрузки категорий из папки backend с файлом manage.py выполните команду:
```
python manage.py add-category
```
- Для загрузки дефолтных данных в базу из папки backend с файлом manage.py выполните команду:
```
python manage.py add_fonts
```
- Для запуска сервера из папки backend с файлом manage.py выполните команду:

```
python manage.py runserver
```

### **API для сервиса "Генератор гармот"** позволяет работать со следующими сущностями:

- Users - Пользователи (зарегистрированные юзеры получают доступ к полному функционалу редактора)

- Documents- Основная сущность - главный продукт приложения. 
Имеет  атрибуты:
    - title - название шаблона формируется по названию JPG-изображения подложки
    - background (подложка в JPG)
    - texts - текстовые поля на документе (Название, ФИО и  др) имеют размер, стиль, шрифт. 
    - elements - ImageField (печати, факсимиле), связано с моделью Element
    - color - цвет подложки, который расчитывается автоматически. Функция фильтрации шаблонов по цветам. 
    - is_horizontal - вертикальное илти горизонтальное расположение подложки документа
    - category - категория документа (грамота, сертификат, благодарность, диплом)

- TextField - сущность для отображения поле texts в Документе
    - text - текст 
    - coordinate_y, coordinate_x - координаты для расположения на документе
    - font - поле, связанное с моделью шрифтов Font
    - font_size, font_color, text_decoration, align  - поля для стилизации текста

- Element - сущность для загрузки и отображения печатей, подписей и т.д.
- Favourite - избранные шаблоны (добавление/удаление)

Предустановленные документы: генерируются по кастомной команде add_fonts, доступны для редактирования пользователями.

**API. Примеры запросов и ответов (в формате json)**

 Регистрация нового пользователя:
POST: /api/auth/regist/ (отправляет письмо с кодом на почту)
~~~
{
  "password": "string",
  "email": "string"
}
~~~
Изменение пароля:
POST: /api/auth/confirm/ (возвращает токен)
~~~
{
  "code": int
}
~~~
Получение списка предустановленных шаблонов (токен не требуется):
GET: /api/documents/
~~~
{
  "count": 10,
    "next": "http://certificates.acceleratorpracticum.ru/api/documents/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Шаблон 1",
            "thumbnail": "http://certificates.acceleratorpracticum.ru/media/thumbnails/template00.jpg",
            "category": 4,
            "color": [
                3,
                7
            ],
            "is_horizontal": false,
            "is_favourite": false
        }
    ]
}
~~~

Создать новый документ:
POST: /api/documents/
~~~
{
  "title": "string",
  "category": 0,
  "is_horizontal": true,
  "texts": [
    {
      "text": "string",
      "coordinate_y": 0,
      "coordinate_x": 0,
      "font": {
        "font": "string",
        "is_bold": true,
        "is_italic": true
      },
      "font_size": 8,
      "font_color": "string",
      "text_decoration": "underline",
      "align": "left"
    }
  ],
  "elements": [
    {
      "image": "string"
      "coordinate_y": 0,
      "coordinate_x": 0
    }
  ]
}
~~~
Загрузить список ФИО в CSV формате :
POST: /api/documents/upload/
~~~
{
  "id": 0,
  "title": "string",
  "thumbnail": "http://example.com",
  "category": 0,
  "color": [
    0
  ],
  "is_horizontal": true,
  "is_favourite": "string"
}
~~~

Скачать документ :
GET: /api/documents/{id}/download/
~~~
{
  "id": 0,
  "user": 0,
  "title": "string",
  "background": "http://example.com",
  "category": 0,
  "color": [
    0
  ],
  "is_horizontal": true,
  "texts": [
    {
      "id": 0,
      "text": "string",
      "coordinate_y": 0,
      "coordinate_x": 0,
      "font": {
        "font": "string",
        "is_bold": true,
        "is_italic": true
      },
      "font_size": 8,
      "font_color": "string",
      "text_decoration": "underline",
      "align": "left"
    }
  ],
  "elements": [
    {
      "coordinate_y": 0,
      "coordinate_x": 0,
      "image": "http://example.com"
    }
  ]
}
~~~

Авторизованным пользователям  доступны все действия с документами, авторами которых они являются. 

Профидль авторизованного пользователя :
GET: /api/profile/
~~~
{
  "count": 0,
  "next": "http://example.com",
  "previous": "http://example.com",
  "results": [
    {
      "id": 0,
      "thumbnail": "http://example.com",
      "is_favourite": "string"
    }
  ]
}
~~~
Добавить документ в избранное:
POST: /api/documents/{id}/favourite/
~~~
{
  "user": 0,
  "document": 0
}
~~~



_Шаблон наполнения env-файла_

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT=5432
SECRET_KEY=
DEBUG=False
```
***IP адресс проекта: http://185.93.111.238/***

***Домен certificates.acceleratorpracticum.ru***

_[Вверх](#anchor)_
