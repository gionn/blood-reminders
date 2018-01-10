from django.shortcuts import render
from django.http import HttpResponse
from .models import Donor
from datetime import datetime,timedelta

def index(request):
    a_month_ago = datetime.now() - timedelta(days=30)
    a_month_ago_sql = a_month_ago.strftime('%Y-%m-%d %H:%M:%S')
    oldest_donations_list = Donor.objects.raw(
    'SELECT * from reminders_donor u \
    LEFT JOIN reminders_donation d ON u.id = d.donor_id \
    LEFT JOIN reminders_reminder r ON u.id = r.donor_id \
    WHERE ( d.done_at < \'{}\' OR NOT EXISTS ( SELECT id FROM reminders_donation d WHERE u.id = d.donor_id  )) \
    AND ( r.sent_at < \'{}\' OR NOT EXISTS ( SELECT id FROM reminders_reminder r WHERE u.id = r.donor_id ))  \
    '.format(a_month_ago_sql,a_month_ago_sql)
    )

    #oldest_donations_list = Donor.objects.filter(
    #    done_at__lte=datetime.now() - timedelta(days=30)
    #).exclude(
    #    donor__reminder__sent_at__gte=datetime.now() - timedelta(days=7)
    #).order_by('done_at')[:5]
    output = ', '.join([d.name for d in oldest_donations_list])
    return HttpResponse(output)
