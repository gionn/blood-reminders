from django.contrib import admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.db.models import F
from django.utils import timezone
from datetime import timedelta

from .models import Donor
from .models import Donation
from .models import Reminder

class NeedsReminderSentFilter(admin.SimpleListFilter):
    title = _('reminder needed')
    parameter_name = 'reminder'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Reminder to be sent')),
            ('false', _('Already reminded')),
        )

    def queryset(self, request, queryset):
        male = Q(gender='M')
        female = Q(gender='F')
        blood_donation = Q(last_donation_type='S')
        plasma_donation = Q(last_donation_type='P')
        not_recent_donation_taken_male = Q(donation__done_at__lte=timezone.now() - timedelta(days=90))
        not_recent_donation_taken_female = Q(donation__done_at__lte=timezone.now() - timedelta(days=180))
        not_recent_plasma_donation_taken = Q(donation__done_at__lte=timezone.now() - timedelta(days=30))
        donation_never_taken = Q(donation__isnull=True)

        not_recent_reminder_sent = Q(reminder__sent_at__lte=timezone.now() - timedelta(days=7))
        reminder_never_sent = Q(reminder__isnull=True)

        if self.value() == 'true':
            return queryset.filter(
                blood_donation & male & not_recent_donation_taken_male | donation_never_taken,
                not_recent_reminder_sent | reminder_never_sent
            ).union(
                Donor.objects.filter(
                    blood_donation & female & not_recent_donation_taken_female | donation_never_taken,
                    not_recent_reminder_sent | reminder_never_sent
                )
            ).union(
                Donor.objects.filter(
                    plasma_donation & not_recent_plasma_donation_taken | donation_never_taken,
                    not_recent_reminder_sent | reminder_never_sent
                )
            ).distinct()
        if self.value() == 'false':
            return queryset.exclude()



class DonorAdmin(admin.ModelAdmin):
    list_filter = (NeedsReminderSentFilter,)
    search_fields = ['name','tax_code']
    ordering = ['-created_at']


class DonationAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-done_at']


class ReminderAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-sent_at']


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Reminder, ReminderAdmin)
