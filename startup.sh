#!/bin/sh -e

if [ -z "${SECRET_KEY}" ]; then
    echo 'SECRET_KEY must be set' >&2
    exit 1
fi

if [ -z "${ADMIN_PASSWORD}" ]; then
    echo 'ADMIN_PASSWORD must be set' >&2
    exit 1
fi

echo 'Migrate database schema'
python manage.py migrate
echo 'Create database superuser'
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USERNAME}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')" || true &> /dev/null
echo 'Collecting static files'
python manage.py collectstatic --noinput
echo 'Run gunicorn'
exec gunicorn blood.wsgi
