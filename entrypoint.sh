#!/bin/sh

# Ждём, пока БД не станет доступной
# (опционально: можно добавить луп с проверкой tcp-порта)
# Здесь можно просто дать задержку, либо использовать подходящий блок попыток.
# sleep 5

# Применяем миграции
python manage.py migrate --noinput

# Если нужно собрать статику (опционально)
# python manage.py collectstatic --noinput

# Запускаем gunicorn (или просто runserver для dev-режима)
#  В ПРОДАКШЕНЕ лучше gunicorn, но для разработки допустим runserver.
#  Ниже — пример для развёртывания через gunicorn:
gunicorn equipment_specs.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120

# Если хотите вместо gunicorn пользоваться встроенным runserver:
# python manage.py runserver 0.0.0.0:8000