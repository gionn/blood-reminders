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
from django.conf import settings


class ChartsView(View):

    def get(self, request, year = None):
        first_donation_date = Donation.objects.order_by('done_at')[0].done_at
        last_donation_date = Donation.objects.order_by('-done_at')[0].done_at
        years_interval = reversed(range(first_donation_date.year, last_donation_date.year + 1))

        if year is not None and year != last_donation_date.year:
            last_update = make_aware(datetime(year, 12, 31))
            current_year = False
        else:
            last_update = Donation.objects.order_by('-done_at')[0].done_at
            current_year = True

        donations_data = self.donations_last_year(Q(), last_update)

        donations_data_male = self.donations_last_year(Q(donor__gender='M'), last_update)

        donations_data_female = self.donations_last_year(Q(donor__gender='F'), last_update)

        donations_yearly_data = Donation.objects.filter(
            done_at__gte=make_aware(datetime(last_update.year - 10, 1, 1)),
            done_at__lt=make_aware(datetime(last_update.year, 1, 1)),
        ).annotate(
            year=TruncYear('done_at')
        ).values('year').annotate(count=Count('id')).values_list('year', 'count').order_by('year')

        blood_type_last_year = Donor.objects.filter(
            last_donation_date__gt=(last_update + relativedelta(months=-12)).replace(day=1, hour=0, minute=0)
        ).values('blood_type', 'blood_rh').annotate(count=Count('id')).values_list('blood_type', 'blood_rh', 'count').order_by('-count')

        age_young_last_year = self.donor_age_count(0, 28, last_update)

        age_junior_last_year = self.donor_age_count(28, 39, last_update)

        age_senior_last_year = self.donor_age_count(39, 50, last_update)

        age_elder_last_year = self.donor_age_count(50, 99, last_update)

        donations_this_year_count = self.donations_this_year_count(last_update)
        donations_this_year_expected = int(settings.DONATIONS_EXPECTED)
        donations_this_year_progress = int(donations_this_year_count * 100 / donations_this_year_expected)

        donations_this_year_remaining = 0
        if (donations_this_year_count < donations_this_year_expected):
            donations_this_year_remaining = donations_this_year_expected - donations_this_year_count

        template = loader.get_template('charts/index.html')
        context = {
            'site_name': settings.SITE_NAME,
            'analytics_code': settings.GA_CODE,
            'donation_type': dict(donation_type),
            'last_update': last_update,
            'year': last_update.year,
            'donations_data': donations_data,
            'donations_data_male': donations_data_male,
            'donations_data_female': donations_data_female,
            'donations_yearly_data': donations_yearly_data,
            'blood_type_last_year': blood_type_last_year,
            'age_last_year': [age_young_last_year, age_junior_last_year, age_senior_last_year, age_elder_last_year],
            'donations_last_year_by_type': self.donations_last_year_by_type(last_update),
            'donations_data_this_year': self.donations_this_year(Q(), last_update),
            'donations_this_year_count': donations_this_year_count,
            'donations_this_year_expected': donations_this_year_expected,
            'donations_this_year_remaining': donations_this_year_remaining,
            'donations_this_year_progress': donations_this_year_progress,
            'donations_data_this_year_projection': self.donations_this_year_projection(last_update),
            'current_year': current_year,
            'years_interval': years_interval,
        }
        return HttpResponse(template.render(context, request))

    def donations_this_year_count(self, date):
        return Donation.objects.filter(
            done_at__gt=make_aware(datetime(date.year, 1, 1)), done_at__lte=make_aware(datetime(date.year, 12, 31))
        ).count()

    def donations_this_year(self, filter_args, date):
        return Donation.objects.filter(
            done_at__gt=make_aware(datetime(date.year, 1, 1)), done_at__lte=make_aware(datetime(date.year, 12, 31))
        ).filter(filter_args).annotate(
            month=TruncMonth('done_at')
        ).values('month').annotate(count=Count('id')).values_list('month', 'count').order_by('month')

    def donations_this_year_projection(self, date):
        result = []
        i = 0
        for count in settings.DONATIONS_PROJECTION.split(','):
            i += 1
            if (i > 12):
                break
            result.append((datetime(date.year, i, 1), int(count)))
        return result

    def donations_last_year(self, filter_args, date):
        return Donation.objects.filter(
            done_at__gte=(date + relativedelta(months=-12)).replace(day=1, hour=0, minute=0),
            done_at__lt=make_aware(datetime(date.year, date.month, 1)),
        ).filter(filter_args).annotate(
            month=TruncMonth('done_at')
        ).values('month').annotate(count=Count('id')).values_list('month', 'count').order_by('month')

    def donations_last_year_by_type(self, date):
        return Donation.objects.filter(
            done_at__gte=(date + relativedelta(months=-12)).replace(day=1, hour=0, minute=0),
            done_at__lt=make_aware(datetime(date.year, date.month, 1)),
        ).values('donation_type').annotate(count=Count('id')).order_by('-count')

    def donor_age_count(self, from_age, to_age, date):
        return Donor.objects.filter(
            last_donation_date__gt=(date+ relativedelta(months=-12)).replace(day=1, hour=0, minute=0),
            born_date__lt=(date + relativedelta(years=-from_age)),
            born_date__gte=(date + relativedelta(years=-to_age))
        ).count()
