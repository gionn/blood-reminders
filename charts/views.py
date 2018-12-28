from django.http import HttpResponse
from django.views import View
from django.template import loader
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from reminders.models import Donation
import datetime

class ChartsView(View):

    def get(self, request):
        last_update = Donation.objects.order_by('-done_at')[0].done_at

        donations_data = Donation.objects.filter(
                done_at__gt=datetime.datetime.now() - datetime.timedelta(weeks=52)
            ).annotate(
                month=TruncMonth('done_at')
            ).values('month').annotate(count=Count('id')).values_list('month','count').order_by('month')

        donations_yearly_data = Donation.objects.filter(
                done_at__gt=datetime.datetime.now() - datetime.timedelta(weeks=52*10)
            ).annotate(
                year=TruncYear('done_at')
            ).values('year').annotate(count=Count('id')).values_list('year','count').order_by('year')

        template = loader.get_template('charts/index.html')
        context = {
            'last_update': last_update,
            'donations_data': donations_data,
            'donations_yearly_data': donations_yearly_data,
        }
        return HttpResponse(template.render(context, request))
