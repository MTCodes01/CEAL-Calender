#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superuser created: admin/admin123');
else:
    print('Superuser already exists');
" || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Start server
echo "Starting Gunicorn..."
exec gunicorn ceal_calendar.wsgi:application --bind 0.0.0.0:8000 --workers 3
