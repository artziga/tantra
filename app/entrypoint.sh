#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd app

poetry run python manage.py migrate --noinput
poetry run python manage.py collectstatic --noinput
#poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000

exec "$@"