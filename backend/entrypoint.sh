#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# If the command is to start the server (default), run migrations first
if [[ "$1" == *"gunicorn"* ]] || [[ "$1" == *"runserver"* ]]; then
    echo "Running migrations..."
    python manage.py migrate --noinput

    # Only create superuser if explicitly enabled (defaults to true for dev)
    if [ "${CREATE_SUPERUSER:-true}" = "true" ]; then
        echo "Checking for superuser..."
        python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@ceal.com').exists():
    User.objects.create_superuser('admin', 'admin@ceal.com', 'adminpassword');
    print('Superuser created: admin@ceal.com/adminpassword');
else:
    print('Superuser already exists');
" || true
    fi

    # Warn if running in DEBUG mode in production
    python manage.py shell -c "
from django.conf import settings;
if settings.DEBUG:
    import logging;
    logging.getLogger('django').warning('⚠️  WARNING: Running with DEBUG=True. Set DEBUG=False for production!');
" || true

    echo "Collecting static files..."
    python manage.py collectstatic --noinput || true
fi

# Execute the passed command
exec "$@"
