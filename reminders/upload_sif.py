import csv
import logging
from datetime import datetime
from io import StringIO

from django.utils import timezone

from .models import Donation, Donor

# Get an instance of a logger
logger = logging.getLogger(__name__)


def parse_donors_file(file):
    csv_file = StringIO(file.read().decode('utf-8-sig'))
    reader = csv.DictReader(csv_file, delimiter=';')
    created = 0
    updated = 0
    for row in reader:
        csv_last_donation_type = get_donation_type(row['Tipo Ultima Donazione'])
        csv_last_donation_date = convert_date(row['Data Ultima Donazione'])
        csv_born_date = convert_date(row['Data Nascita'])
        csv_blood_type = convert_blood_type(row['Gruppo sanguigno'])
        csv_blood_rh = convert_rh(row['Rh'])
        phone = convert_phone(row['Recapiti telefonici'])

        try:
            existing_donor = Donor.objects.get(tax_code=row['Codice Fiscale'])
            existing_donor.last_donation_type = csv_last_donation_type
            existing_donor.last_donation_date = csv_last_donation_date
            existing_donor.blood_type = csv_blood_type
            existing_donor.blood_rh = csv_blood_rh
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
                blood_type=csv_blood_type,
                blood_rh=csv_blood_rh,
                last_donation_type=csv_last_donation_type,
                last_donation_date=csv_last_donation_date,
                phone=phone,
                email=row['Recapiti mail'],
            )
            d.save()
            created += 1
    logger.info('Finished importing: {} creation, {} update'.format(created, updated))


def parse_donations_file(file):
    last_tracked_donation = get_last_donation_date()
    csv_file = StringIO(file.read().decode('utf-8-sig'))
    reader = csv.DictReader(csv_file, delimiter=';')
    created = 0
    for row in reader:
        csv_donation_date = convert_date(row['Data'])
        if csv_donation_date < last_tracked_donation:
            continue
        csv_born_date = convert_date(row['Data Nascita'])
        try:
            existing_donor = Donor.objects.get(name=row['Donatore'], born_date=csv_born_date)
            Donation.objects.get(
                donor=existing_donor,
                done_at=csv_donation_date
            )
            continue
        except Donor.DoesNotExist:
            logger.warning('''{} is not an existing donor'''.format(row['Donatore']))
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
    logger.info('Finished importing donations: {} created'.format(created))


def get_donation_type(input):
    output = ''
    if input == 'Sangue intero':
        output = 'B'
    elif input == 'Plasmaferesi':
        output = 'P'
    elif input == 'Multicomponent':
        output = 'M'
    else:
        logger.warning('Unrecognized value "{}"'.format(input))
    return output


def convert_blood_type(input):
    output = ''
    if input == '0' or input == 'O':
        output = 'O'
    elif input == 'A':
        output = 'A'
    elif input == 'B':
        output = 'B'
    elif input == 'AB':
        output = 'AB'
    else:
        logger.warning('Unrecognized value "{}"'.format(input))
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
    logger.warning('Unrecognized rh {}'.format(string))


def convert_phone(string):
    phone = string.split(';')[0]
    if phone and not phone.startswith('+'):
        phone = '+39' + phone
    return phone


def get_last_donation_date():
    query = Donation.objects.order_by('-done_at')
    if query:
        return query[0].done_at
    else:
        return timezone.make_aware(datetime(1900, 1, 1))
