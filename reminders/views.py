from django.shortcuts import render
from django.http import HttpResponse
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
        logger.warn('is a post')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.warn('is valid')
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/admin/')
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
        
        d = Donor(
            name=row['Soggetto'],
            tax_code=row['Codice Fiscale'],
            gender=row['Sesso'],
            last_donation_type=csv_last_donation_type,
            phone=row['Recapiti telefonici'],
            email=row['Recapiti mail'],
        )
        d.save()