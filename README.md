# Fratres blood reminders

A web application to remind people that they can do a new donation after a time frame.

This has been developed inside my local [FRATRES](http://www.fratres.org) group to help the reminding process of the donors.

This is my first django / python application, please be gently.

## Current features

* Admin panel with user/password authentication [screenshot](screenshots/admin-home.jpeg)
* Support import from Fratres SIF software CSV of donors (Informazioni Associati -> Soci and Cessati) and donations (Informazioni Donatori -> Donazioni)
* Donor management (personal data, contact information, blood type) [screenshot 1](screenshots/donors-list.jpeg) [screenshot 2](screenshots/donors-edit-1.jpeg) [screenshot 3](screenshots/donors-edit-2.jpeg)
* Donations management
* Reminders management (not really sending any reminder) [screenshot](screenshots/create-reminder.jpeg)
* Public charts page with Chart.js [screenshot](screenshots/charts.jpeg)

## Roadmap

* Sending personal reminders via SMS
* Sending personal reminders via WhatsApp
* Sending reminders automatically based on a schedule
* Sending reminders based on current blood availability (https://web2.e.toscana.it/crs/meteo/)

## Usage (docker-composer)

Configure the following environment variables in a .env file:

```bash
SECRET_KEY=kahlaiwoopeex2ooQuoTei2ch
DB_NAME=reminders
DB_USER=reminders
DB_PASS=to6oc9Ahl6oogei
DB_HOST=db
DB_PORT=5432
DB_PATH=./pgdata
ADMIN_PASSWORD=changeme
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
```

Build and run with docker-composer:

```sh
docker-compose up --build
```

Access admin panel at [localhost:8000/admin](http://localhost:8000/admin/)

Default credentials:

* username: admin
* password: changeme

### Docker environment variables reference

* SECRET_KEY: generate one [here](https://www.miniwebtool.com/django-secret-key-generator/)
* ADMIN_USERNAME: the username of the first created superadmin user (default: admin)
* ADMIN_PASSWORD: the password of the first created superadmin user (default: changeme)
* ADMIN_EMAIL: the email of the first created superadmin user (default: admin@change.me)
* DB_*: configures postgres container
* DONATIONS_PROJECTION: in the charts page, used by the first chart to draw a line as a target donation for every mounth (comma separated integers)
* DONATIONS_EXPECTED: in the charts page, used by the second chart for the target amount of yearly donations for the current year.
* APP_LOG_LEVEL: configure default logging level (defaults to INFO)

## Development

```bash
# Python Dependencies
apt-get install libpq-dev
pip install -r requirements.txt

# Project dependencies (postgres)
docker-compose -f docker-compose.dev.yml up -d

# Upgrade the database schema
python manage.py migrate

# Creates an admin account
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USERNAME}', '${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')" || true &> /dev/null

# go django go
python manage.py runserver
```
