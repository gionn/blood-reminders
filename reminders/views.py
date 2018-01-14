from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
from django.db.models import F

from .models import Donor
from django.utils import timezone
from datetime import timedelta

from .forms import UploadFileForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/reminders/')
    else:
        form = UploadFileForm()
    logger.info('rendering form')
    return render(request, 'upload.html', {'form': form})


import csv
from io import StringIO
from reminders.models import Donor

def handle_uploaded_file(file):
    csv_file = StringIO(file.read().decode())
    reader = csv.DictReader(csv_file,delimiter=';')
    created = 0
    updated = 0
    for row in reader:
        csv_last_donation_type = ''
        if row['Tipo Ultima Donazione'] == 'Sangue intero':
            csv_last_donation_type = 'S'
        elif row['Tipo Ultima Donazione'] == 'Plasmaferesi':
            csv_last_donation_type = 'P'
        elif row['Tipo Ultima Donazione'] == 'Multicomponent':
            csv_last_donation_type = 'M'
        else:
            logger.warn('Unrecognized value "{}"'.format(row['Tipo Ultima Donazione']))

        split_phone = row['Recapiti telefonici'].split(';')[0]

        try:
            existing_donor = Donor.objects.get(tax_code=row['Codice Fiscale'])
            existing_donor.last_donation_type = csv_last_donation_type
            existing_donor.phone=split_phone
            existing_donor.email=row['Recapiti mail']
            existing_donor.save()
            updated += 1
        except Donor.DoesNotExist:
            d = Donor(
                name=row['Soggetto'],
                tax_code=row['Codice Fiscale'],
                gender=row['Sesso'],
                last_donation_type=csv_last_donation_type,
                phone=split_phone,
                email=row['Recapiti mail'],
            )
            d.save()
            created += 1
    logger.warn('Finished importing: {} creation, {} update'.format(created,updated))