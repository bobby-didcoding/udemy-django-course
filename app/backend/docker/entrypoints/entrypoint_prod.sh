#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py test
# python manage.py collectstatic --noinput

exec "$@"
