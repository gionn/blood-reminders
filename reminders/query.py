from django.db.models import Max, Q
from django.utils import timezone
from datetime import timedelta
from .models import BLOOD_TYPE, PLASMA_TYPE, MULTIC_TYPE


class DonorQuerySet():
    def get_base_queryset(self):
        male = Q(gender='M')
        female = Q(gender='F')
        blood_donation = Q(last_donation_type=BLOOD_TYPE)
        plasma_donation = Q(last_donation_type=PLASMA_TYPE) | Q(last_donation_type=MULTIC_TYPE)
        not_recent_donation_taken_male = Q(last_donation__lte=timezone.now() - timedelta(days=90))
        not_recent_donation_taken_female = Q(last_donation__lte=timezone.now() - timedelta(days=180))
        not_recent_plasma_donation_taken = Q(last_donation__lte=timezone.now() - timedelta(days=30))
        not_suspended = Q(suspension_date__lte=timezone.now()) | Q(suspension_date__isnull=True)

        donation_never_taken = Q(donation__isnull=True)
        not_recent_reminder_sent = Q(reminder__sent_at__lte=timezone.now() - timedelta(days=21))
        reminder_never_sent = Q(reminder__isnull=True)

        return (
            (blood_donation & male & not_recent_donation_taken_male) |
            (blood_donation & female & not_recent_donation_taken_female) |
            (plasma_donation & not_recent_plasma_donation_taken)
        ) & not_suspended & (
            (not_recent_reminder_sent | reminder_never_sent) | donation_never_taken
        )

    def get_donors_with_reminders(self, queryset):
        restriction = self.get_base_queryset()
        return queryset.annotate(
            last_donation=Max('donation__done_at')
        ).filter(restriction).distinct()

    def get_donors_without_reminders(self, queryset):
        restriction = self.get_base_queryset()
        return queryset.annotate(
            last_donation=Max('donation__done_at')
        ).exclude(restriction).distinct()
