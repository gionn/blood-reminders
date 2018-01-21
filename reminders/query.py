from django.db.models import Q,F,Max
from django.utils import timezone
from datetime import timedelta

class DonorQuerySet():
    def get_base_queryset(self):
        male = Q(gender='M')
        female = Q(gender='F')
        blood_donation = Q(last_donation_type='S')
        plasma_donation = Q(last_donation_type='P')
        not_recent_donation_taken_male = Q(last_donation__lte=timezone.now() - timedelta(days=90))
        not_recent_donation_taken_female = Q(last_donation__lte=timezone.now() - timedelta(days=180))
        not_recent_plasma_donation_taken = Q(last_donation__lte=timezone.now() - timedelta(days=30))
        has_recent_donations = Q(last_donation__gte=timezone.now() - timedelta(days=720))

        donation_never_taken = Q(donation__isnull=True)
        not_recent_reminder_sent = Q(reminder__sent_at__lte=timezone.now() - timedelta(days=7))
        reminder_never_sent = Q(reminder__isnull=True)

        return ( 
            ( blood_donation & male & not_recent_donation_taken_male ) |
            ( blood_donation & female & not_recent_donation_taken_female ) |
            ( plasma_donation & not_recent_plasma_donation_taken )
        ) & has_recent_donations & ( not_recent_reminder_sent | reminder_never_sent ) | donation_never_taken

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