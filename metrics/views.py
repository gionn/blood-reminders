from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from prometheus_client import generate_latest, CollectorRegistry
from reminders.models import Donation, Donor
import prometheus_client
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY


class CustomCollector(object):
    def collect(self):
        donations = GaugeMetricFamily("donations", "How many donations", labels=['type'])
        donations.add_metric(['blood'], Donation.objects.filter(donation_type='B').count())
        donations.add_metric(['plasma'], Donation.objects.filter(donation_type='P').count())
        donations.add_metric(['multic'], Donation.objects.filter(donation_type='M').count())
        yield donations

        donors = GaugeMetricFamily("donors", "How many donors", labels=['gender', 'blood_type', 'blood_rh'])
        for gender in ['M', 'F']:
            for blood_type in ['O', 'A', 'B', 'AB']:
                for blood_rh in ['+', '-']:
                    value = Donor.objects.filter(gender=gender, blood_type=blood_type, blood_rh=blood_rh).count()
                    donors.add_metric([gender, blood_type, blood_rh], value)
        yield donors

class MetricsView(View):

    def get(self, request):
        registry = CollectorRegistry()
        registry.register(CustomCollector())
        data = generate_latest(registry)
        return HttpResponse(
            data,
            content_type=prometheus_client.CONTENT_TYPE_LATEST)




