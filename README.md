# Fratres blood reminders

[![Docker Build Status](https://img.shields.io/docker/build/gionn/blood-reminders.svg)]() [![Docker Automated build](https://img.shields.io/docker/automated/gionn/blood-reminders.svg)]()

A web application to remind people that they can do a new donation after a time frame.

This has been developed inside my local [FRATRES](http://www.fratres.org) group to help the reminding process of the donors.

This is my first django / python application, please be gently.

## Current features

* Admin panel with user/password authentication [screenshot](screenshots/admin-home.jpeg)
* Support CSV import of donors and donations from existing FRATRES SIF software
* Donor management (personal data, contact information, blood type) [screenshot 1](screenshots/donors-list.jpeg) [screenshot 2](screenshots/donors-edit-1.jpeg) [screenshot 3](screenshots/donors-edit-2.jpeg)
* Donations management
* Reminders management (not really sending any reminder) [screenshot](screenshots/create-reminder.jpeg)

## Roadmap

* Sending personal reminders via SMS
* Sending personal reminders via WhatsApp
* Sending reminders automatically based on a schedule
* Sending reminders based on current blood availability (https://web2.e.toscana.it/crs/meteo/)

## Usage (docker-composer)

Configure the following environment variables (e.g. in a .env file):

```
SECRET_KEY=kahlaiwoopeex2ooQuoTei2ch
DB_NAME=reminders
DB_USER=reminders
DB_PASS=to6oc9Ahl6oogei
DB_HOST=db
DB_PORT=5432
DB_PATH=./pgdata
ADMIN_PASSWORD=changeme
```

Build and run with docker-composer:

    docker-compose up --build

Access http://localhost:8000/admin/

Default credentials:

* username: admin
* password: changeme

### Docker environment variables reference

* SECRET_KEY: generate one [here](https://www.miniwebtool.com/django-secret-key-generator/)
* ADMIN_USERNAME: the username of the first created superadmin user (default: admin)
* ADMIN_PASSWORD: the password of the first created superadmin user (default: changeme)
* ADMIN_EMAIL: the email of the first created superadmin user (default: admin@change.me)
* DB_*: configures postgres container

## Development

    docker-compose -f docker-compose.develop.yml up
    python manage.py runserver
