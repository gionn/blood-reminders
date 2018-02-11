import csv
import logging
from datetime import datetime
from io import StringIO

from django.utils import timezone

from reminders.models import Donation, Donor

from .models import Donor

# Get an instance of a logger
logger = logging.getLogger(__name__)


def handle_uploaded_donors_file(file):
    csv_file = StringIO(file.read().decode())
    reader = csv.DictReader(csv_file, delimiter=';')
    created = 0
    updated = 0
    for row in reader:
        csv_last_donation_type = get_donation_type(row['Tipo Ultima Donazione'])
        csv_last_donation_date = convert_date(row['Data Ultima Donazione'])
        csv_born_date = convert_date(row['Data Nascita'])
        phone = convert_phone(row['Recapiti telefonici'])

        try:
            existing_donor = Donor.objects.get(tax_code=row['Codice Fiscale'])
            existing_donor.last_donation_type = csv_last_donation_type
            existing_donor.last_donation_date = csv_last_donation_date
            if not existing_donor.phone or not existing_donor.phone.startswith('+'):
                existing_donor.phone = phone
            if not existing_donor.email:
                existing_donor.email = row['Recapiti mail']
            existing_donor.save()
            updated += 1
        except Donor.DoesNotExist:
            d = Donor(
                name=row['Soggetto'],
                tax_code=row['Codice Fiscale'],
                born_date=csv_born_date,
                gender=row['Sesso'],
                blood_type=row['Gruppo sanguigno'],
                blood_rh=convert_rh(row['Rh']),
                last_donation_type=csv_last_donation_type,
                last_donation_date=csv_last_donation_date,
                phone=phone,
                email=row['Recapiti mail'],
            )
            d.save()
            created += 1
    logger.warn('Finished importing: {} creation, {} update'.format(created, updated))


def handle_uploaded_donations_file(file):
    csv_file = StringIO(file.read().decode())
    reader = csv.DictReader(csv_file, delimiter=';')
    created = 0
    for row in reader:
        csv_donation_date = convert_date(row['Data'])
        csv_born_date = convert_date(row['Data Nascita'])
        try:
            existing_donor = Donor.objects.get(name=row['Donatore'], born_date=csv_born_date)
            existing_donation = Donation.objects.get(
                donor=existing_donor,
                done_at=csv_donation_date
            )
            continue
        except Donor.DoesNotExist:
            continue
        except Donation.DoesNotExist:
            existing_donor = Donor.objects.get(name=row['Donatore'], born_date=csv_born_date)
            csv_donation_type = get_donation_type(row['Tipo donazione'])
            d = Donation(
                donor=existing_donor,
                done_at=csv_donation_date,
                donation_type=csv_donation_type,
            )
            d.save()
            created += 1
    logger.warn('Finished importing donations: {} created'.format(created))


def get_donation_type(input):
    output = ''
    if input == 'Sangue intero':
        output = 'B'
    elif input == 'Plasmaferesi':
        output = 'P'
    elif input == 'Multicomponent':
        output = 'M'
    else:
        logger.warn('Unrecognized value "{}"'.format(input))
    return output


def convert_date(date_string):
    if not date_string:
        return None
    date = datetime.strptime(date_string, '%d/%m/%Y')
    current_tz = timezone.get_current_timezone()
    return current_tz.localize(date)


def convert_rh(string):
    if not string:
        return ''
    if string.lower() == 'positivo':
        return '+'
    if string.lower() == 'negativo':
        return '-'
    logger.warn('unhandled rh {}'.format(string))


def convert_phone(string):
    phone = string.split(';')[0]
    if phone and not phone.startswith('+'):
        phone = '+39' + phone
    return phone
