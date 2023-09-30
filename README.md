# Back

![example workflow](https://github.com/certificates-and-commendations/Back/actions/workflows/certificates_deploy.yml/badge.svg)

## Описание

Благодаря этому проекту можно создавать грамоты, дипломы, благодарности и сертификаты.

### Технологии

Python 3.9.10

Django 3.2

djangorestframework 3.14.0

### Инфраструктура: 
* Docker
* NGINX
* GUNICORN
* база даннных POSTGRESQL

### Запуск проекта в dev-режиме

- Установите и активируйте виртуальное окружение, утановите pip

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