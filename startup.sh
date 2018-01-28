#!/bin/sh
python manage.py migrate
exec gunicorn blood.wsgi