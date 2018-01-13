from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import F

from .models import Donor
from django.utils import timezone
from datetime import timedelta

def index(request):
    not_recent_donation_taken = Q(donation__done_at__lte=timezone.now() - timedelta(days=30))
    donation_never_taken = Q(donation__isnull=True)

    not_recent_reminder_sent = Q(reminder__sent_at__lte=timezone.now() - timedelta(days=7))
    reminder_never_sent = Q(reminder__isnull=True)

    oldest_donations_list = Donor.objects.filter(
        not_recent_donation_taken | donation_never_taken,
        not_recent_reminder_sent | reminder_never_sent
    ).order_by('created_at')[:5]

    output = ', '.join([d.name for d in oldest_donations_list])
    return HttpResponse(output)
