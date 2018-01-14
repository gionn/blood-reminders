from django.db import models
from django.utils import timezone

class Donor(models.Model):
    name = models.CharField(max_length=200)
    tax_code = models.CharField(max_length=16,unique=True)
    born_date = models.DateTimeField(default='1970-01-01 00:00')
    gender = models.CharField(max_length=1,choices=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Undefined'),
    ))
    last_donation_type = models.CharField(max_length=1,blank=True,choices=(
        ('S', 'Sangue Intero'),
        ('P', 'Plasmaferesi'),
        ('M', 'Multicomponent')
    ))
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    done_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    donation_type = models.CharField(max_length=1,blank=True,choices=(
        ('S', 'Sangue Intero'),
        ('P', 'Plasmaferesi'),
        ('M', 'Multicomponent')
    ))

    def __str__(self):
        return 'donation of ' + self.donor.name + ' at ' + self.done_at.strftime('%d %B %Y')


class Reminder(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'reminder for ' + self.donor.name + ' at ' + self.sent_at.strftime('%d %B %Y')
