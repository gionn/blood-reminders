import csv
from datetime import datetime
from io import StringIO

from django.utils import timezone
from django.contrib import messages

from reminders.models import Donation, Donor

from .models import Donor

def handle_uploaded_donors_file(file, request):
    csv_file = StringIO(file.read().decode('utf-8-sig'))
    reader = csv.DictReader(csv_file, delimiter=';')
    created = 0
    updated = 0
    for row in reader:
        discontinued_donor = 'Data cessazione' in row
        if discontinued_donor:
            csv_suspension_date = convert_date(row['Data cessazione'])
        else:
            csv_last_donation_type = convert_donation_type(row['Tipo Ultima Donazione'], request)
            csv_last_donation_date = convert_date(row['Data Ultima Donazione'])

        csv_born_date = convert_date(row['Data Nascita'])
        csv_blood_type = convert_blood_type(row['Gruppo sanguigno'], request)
        csv_blood_rh = convert_rh(row['Rh'], request)
        phone = convert_phone(row['Recapiti telefonici'])

        try:
            existing_donor = Donor.objects.get(tax_code=row['Codice Fiscale'])
            if discontinued_donor:
                existing_donor.suspension_date = csv_suspension_date
                existing_donor.suspension_reason = 'discontinued'
            else:
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
            new_donor = Donor(
                name=row['Soggetto'],
                tax_code=row['Codice Fiscale'],
                born_date=csv_born_date,
                gender=row['Sesso'],
                blood_type=csv_blood_type,
                blood_rh=csv_blood_rh,
                phone=phone,
                email=row['Recapiti mail'],
            )
            if discontinued_donor:
                new_donor.suspension_date = csv_suspension_date
                new_donor.suspension_reason = 'discontinued'
            else:
                new_donor.last_donation_type = csv_last_donation_type
                new_donor.last_donation_date = csv_last_donation_date
            new_donor.save()
            created += 1
    messages.info(request, 'Import successful: {} created, {} updated'.format(created, updated))


def handle_uploaded_donations_file(file, request):
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
            messages.warning(request, '''{} is not an existing donor, skipping donation of {}'''.format(row['Donatore'], csv_donation_date))
            continue
        except Donation.DoesNotExist:
            existing_donor = Donor.objects.get(name=row['Donatore'], born_date=csv_born_date)
            csv_donation_type = convert_donation_type(row['Tipo donazione'], request)
            d = Donation(
                donor=existing_donor,
                done_at=csv_donation_date,
                donation_type=csv_donation_type,
            )
            d.save()
            created += 1
    messages.info(request, 'Import successful: {} created'.format(created))


def convert_donation_type(string, request):
    if not string.strip():
        return None
    if string == 'Sangue intero':
        return 'B'
    elif string == 'Plasmaferesi':
        return 'P'
    elif string == 'Multicomponent':
        return 'M'
    messages.warning(request, 'Unrecognized donation type for value <{}>'.format(string))


def convert_blood_type(string, request):
    if not string.strip() or string == 'NS':
        return None
    elif string == '0' or string == 'O':
        return 'O'
    elif string == 'A':
        return 'A'
    elif string == 'B':
        return 'B'
    elif string == 'AB':
        return 'AB'
    messages.warning(request, 'Unrecognized blood type for value <{}>'.format(string))


def convert_date(date_string):
    if not date_string.strip():
        return None
    date = datetime.strptime(date_string, '%d/%m/%Y')
    current_tz = timezone.get_current_timezone()
    return current_tz.localize(date)


def convert_rh(string, request):
    if not string.strip() or string == 'NS':
        return None
    if string.lower() == 'positivo':
        return '+'
    if string.lower() == 'negativo':
        return '-'
    messages.warning(request, 'Unrecognized rh for value <{}>'.format(string))


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
