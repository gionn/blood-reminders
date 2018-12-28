from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncYear
from reminders.models import Donation, Donor
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class ChartsView(View):

    def get(self, request):
        last_update = Donation.objects.order_by('-done_at')[0].done_at

        now = timezone.now()

        donations_data = self.donations_last_year(Q())

        donations_data_male = self.donations_last_year(Q(donor__gender='M'))

        donations_data_female = self.donations_last_year(Q(donor__gender='F'))

        donations_yearly_data = Donation.objects.filter(
                done_at__gt=make_aware(datetime(now.year - 10, 1, 1))
            ).annotate(
                year=TruncYear('done_at')
            ).values('year').annotate(count=Count('id')).values_list('year','count').order_by('year')

        blood_type_last_year = Donor.objects.filter(
                last_donation_date__gt=(timezone.now() + relativedelta(months=-12)).replace(day=1, hour=0, minute=0)
            ).values('blood_type','blood_rh').annotate(count=Count('id')).values_list('blood_type','blood_rh','count').order_by('-count')

        template = loader.get_template('charts/index.html')
        context = {
            'last_update': last_update,
            'donations_data': donations_data,
            'donations_data_male': donations_data_male,
            'donations_data_female': donations_data_female,
            'donations_yearly_data': donations_yearly_data,
            'blood_type_last_year': blood_type_last_year,
        }
        return HttpResponse(template.render(context, request))

    def donations_last_year(self, filter_args):
        return Donation.objects.filter(
                done_at__gt=(timezone.now() + relativedelta(months=-12)).replace(day=1, hour=0, minute=0)
            ).filter(filter_args).annotate(
                month=TruncMonth('done_at')
            ).values('month').annotate(count=Count('id')).values_list('month','count').order_by('month')
