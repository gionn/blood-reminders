from django.contrib import admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Donor
from .models import Donation
from .models import Reminder

from reminders.query import DonorQuerySet

import logging

logger = logging.getLogger(__name__)

class NeedsReminderSentFilter(admin.SimpleListFilter):
    title = _('reminder needed')
    parameter_name = 'reminder'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Reminder to be sent')),
            ('false', _('Reminder not needed')),
        )

    def queryset(self, request, queryset):
        donor_queryset = DonorQuerySet()
        if self.value() == 'true':
            queryset = donor_queryset.get_donors_with_reminders(queryset)
            logger.warn(queryset.query)
            return queryset
        if self.value() == 'false':
            return donor_queryset.get_donors_without_reminders(queryset)


class DonorAdmin(admin.ModelAdmin):
    list_filter = (NeedsReminderSentFilter,)
    search_fields = ['name','tax_code']
    ordering = ['-created_at']
    list_display = ('name', 'gender', 'last_donation_type', 'last_donation_date')


class DonationAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-done_at']
    list_display = ('donor', 'done_at_pretty', 'donation_type')


class ReminderAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-sent_at']


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.site_header = 'Blood donors messaging system'
