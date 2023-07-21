#!/bin/sh
python manage.stage.py makemigrations
python manage.stage.py migrate
python manage.stage.py test
# python manage.py collectstatic --noinput

exec "$@"

