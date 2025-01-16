#!/bin/bash
set -e

echo "Starting ..."

cd well_prepared

PORT=${PORT:-8000}
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-well_prepared.settings_prod}
export DJANGO_SETTINGS_MODULE

uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
exec uv run gunicorn well_prepared.wsgi -w 3 --threads 3 -b "0.0.0.0:$PORT"
