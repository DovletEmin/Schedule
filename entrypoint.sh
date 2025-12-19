#!/bin/sh
set -e

# Wait for DB / apply migrations, collect static, then start Gunicorn
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn src.wsgi:application --bind 0.0.0.0:${PORT:-80} --workers 3
