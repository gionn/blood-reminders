from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_date
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncYear
from reminders.models import Donation, Donor, donation_type
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class ChartsView(View):

    now = timezone.now()

    def get(self, request):
        last_update = Donation.objects.order_by('-done_at')[0].done_at

        donations_data = self.donations_last_year(Q())

        donations_data_male = self.donations_last_year(Q(donor__gender='M'))

        donations_data_female = self.donations_last_year(Q(donor__gender='F'))

        donations_yearly_data = Donation.objects.filter(
                done_at__gt=make_aware(datetime(self.now.year - 10, 1, 1))
            ).annotate(
                year=TruncYear('done_at')
            ).values('year').annotate(count=Count('id')).values_list('year','count').order_by('year')

        blood_type_last_year = Donor.objects.filter(
                last_donation_date__gt=(self.now + relativedelta(months=-12)).replace(day=1, hour=0, minute=0)
            ).values('blood_type','blood_rh').annotate(count=Count('id')).values_list('blood_type','blood_rh','count').order_by('-count')

        age_young_last_year = self.donor_age_count(0, 28)

        age_junior_last_year = self.donor_age_count(28, 39)

        age_senior_last_year = self.donor_age_count(39, 50)

        age_elder_last_year = self.donor_age_count(50, 99)

        template = loader.get_template('charts/index.html')
        context = {
            'donation_type': dict(donation_type),
            'last_update': last_update,
            'donations_data': donations_data,
            'donations_data_male': donations_data_male,
            'donations_data_female': donations_data_female,
            'donations_yearly_data': donations_yearly_data,
            'blood_type_last_year': blood_type_last_year,
            'age_last_year': [age_young_last_year, age_junior_last_year, age_senior_last_year, age_elder_last_year],
            'donations_this_month': self.donations_this_month(),
        }
        return HttpResponse(template.render(context, request))

    def donations_this_month(self):
        return Donation.objects.filter(
                done_at__gte=make_aware(datetime(self.now.year, self.now.month, 1))
            ).values('donation_type').annotate(count=Count('id'))

    def donations_last_year(self, filter_args):
        return Donation.objects.filter(
                done_at__gt=(timezone.now() + relativedelta(months=-12)).replace(day=1, hour=0, minute=0)
            ).filter(filter_args).annotate(
                month=TruncMonth('done_at')
            ).values('month').annotate(count=Count('id')).values_list('month','count').order_by('month')

    def donor_age_count(self, from_age, to_age):
        return Donor.objects.filter(
                last_donation_date__gt=(timezone.now() + relativedelta(months=-12)).replace(day=1, hour=0, minute=0),
                born_date__lt=(timezone.now() + relativedelta(years=-from_age)),
                born_date__gte=(timezone.now() + relativedelta(years=-to_age))
            ).count()
