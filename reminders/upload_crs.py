import logging
from datetime import datetime
from io import StringIO

from django.utils import timezone

from .models import Donation, Donor

# Get an instance of a logger
logger = logging.getLogger(__name__)


def handle_uploaded_donors_file(file):
    txt_file = StringIO(file.read().decode('utf-8-sig'))
    for line in txt_file:
