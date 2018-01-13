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
        not_recent_donation_taken = Q(donation__done_at__lte=timezone.now() - timedelta(days=30))
        donation_never_taken = Q(donation__isnull=True)

        not_recent_reminder_sent = Q(reminder__sent_at__lte=timezone.now() - timedelta(days=7))
        reminder_never_sent = Q(reminder__isnull=True)

        if self.value() == 'true':
            return queryset.filter(
                not_recent_donation_taken | donation_never_taken,
                not_recent_reminder_sent | reminder_never_sent
            )
        if self.value() == 'false':
            return queryset.exclude(
                not_recent_donation_taken | donation_never_taken,
                not_recent_reminder_sent | reminder_never_sent
            )


class DonorAdmin(admin.ModelAdmin):
    list_filter = (NeedsReminderSentFilter,)


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation)
admin.site.register(Reminder)
