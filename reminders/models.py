from django.db import models
from django.utils import timezone

class Donor(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    done_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return 'donation of ' + self.donor.name + ' at ' + self.done_at.strftime('%d %B %Y')


class Reminder(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'reminder for ' + self.donor.name + ' at ' + self.sent_at.strftime('%d %B %Y')
