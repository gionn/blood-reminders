# Fratres blood reminders

A web application to remind people that they can do a new donation after a time frame.

This has been developed inside my local [FRATRES](http://www.fratres.org) group to help the reminding process of the donors.

This is my first django / python application, please be gently.

## Current features

* Support CSV import of donors and donations from existing FRATRES SIF software
* Donor management (personal data, contact information, blood type)
* Donations management
* Reminders management (not really sending any reminder)

## Roadmap

* Sending personal reminders via SMS
* Sending personal reminders via WhatsApp
* Sending reminders automatically based on a schedule

## Usage (docker)

Build and run with docker-composer:

    docker-compose up --build


Use prebuilt image:

    docker run -e SECRET_KEY='a-random-secret-key' gionn/blood-reminders

Access http://localhost/admin/

### Docker environment variables

* SECRET_KEY: generate one [here](https://www.miniwebtool.com/django-secret-key-generator/)
* ADMIN_USERNAME: the username of the first created superadmin user (default: admin)
* ADMIN_PASSWORD: the password of the first created superadmin user (default: changeme)
* ADMIN_EMAIL: the email of the first created superadmin user (default: admin@change.me)