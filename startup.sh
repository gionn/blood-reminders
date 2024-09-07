#!/bin/sh -e
echo 'Migrate database schema'
python manage.py migrate
echo 'Create database superuser'
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USERNAME}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')" || true &> /dev/null
echo 'Collecting static files'
python manage.py collectstatic --noinput
echo 'Run gunicorn'
exec gunicorn blood.wsgi
