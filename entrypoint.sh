#!/bin/sh

# exit on errors
set -e

# collectstatic if needed
if [ "$DJANGO_COLLECTSTATIC" = "1" ]; then
  echo "Collecting static files"
  python manage.py collectstatic --noinput
fi

# apply database migrations
echo "Applying database migrations"
python manage.py migrate --noinput

# run whatever CMD was passed (gunicorn in Dockerfile)
exec "$@"
