from django.test import TestCase
from django.utils import timezone

from reminders.models import Donation, Donor


class ChartsViewTest(TestCase):

    def test_charts_page_renders_with_a_donation(self):
        donor = Donor.objects.create(name='Test donor', tax_code='TESTCODE', gender='M')
        Donation.objects.create(donor=donor, done_at=timezone.now())

        response = self.client.get('/charts/')

        self.assertEqual(response.status_code, 200)
