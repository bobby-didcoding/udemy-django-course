#!/bin/sh
python manage.prod.py makemigrations
python manage.prod.py migrate
python manage.prod.py test
# python manage.py collectstatic --noinput

exec "$@"
