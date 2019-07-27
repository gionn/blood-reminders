from django.test import TestCase
from reminders.models import Donor, Donation, BLOOD_TYPE
from reminders.query import DonorQuerySet
from django.utils import timezone
from datetime import timedelta


class DonorTestCase(TestCase):
    queryset = DonorQuerySet()
    base = Donor.objects.all()

    def test_empty(self):
        self.assertEqual(self.queryset.get_donors_with_reminders(self.base).count(), 0)
        self.assertEqual(self.queryset.get_donors_without_reminders(self.base).count(), 0)

    def test_male_donor_with_old_blood_donations(self):
        donor = self.donor('male blood', 'M', BLOOD_TYPE)
        self.donation(donor, 100, BLOOD_TYPE)
        self.donation(donor, 365, BLOOD_TYPE)
        self.assertEqual(self.queryset.get_donors_with_reminders(self.base).count(), 1)

    def test_female_donor_with_old_blood_donations(self):
        donor = self.donor('female blood', 'F', BLOOD_TYPE)
        self.donation(donor, 181, BLOOD_TYPE)
        self.donation(donor, 365, BLOOD_TYPE)
        self.assertEqual(self.queryset.get_donors_with_reminders(self.base).count(), 1)

    def test_male_donor_with_recent_blood_donations(self):
        donor = self.donor('male blood', 'M', BLOOD_TYPE)
        self.donation(donor, 10, BLOOD_TYPE)
        self.donation(donor, 100, BLOOD_TYPE)
        self.donation(donor, 365, BLOOD_TYPE)
        self.assertEqual(self.queryset.get_donors_with_reminders(self.base).count(), 0)

    def donor(self, name, gender, donation_type):
        return Donor.objects.create(
            name=name,
            gender=gender,
            last_donation_type=donation_type
        )

    def donation(self, donor, days, donation_type):
        return Donation.objects.create(
            donor=donor,
            donation_type=donation_type,
            done_at=timezone.now() - timedelta(days=days)
        )
