from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

BLOOD_TYPE = 'B'
PLASMA_TYPE = 'P'
MULTIC_TYPE = 'M'

donation_type = (
    (BLOOD_TYPE, _('Blood')),
    (PLASMA_TYPE, _('Plasma')),
    (MULTIC_TYPE, _('Multicomponent'))
)


class Donor(models.Model):
    name = models.CharField(_('name'), max_length=200)
    tax_code = models.CharField(_('tax code'), max_length=16, unique=True)
    born_date = models.DateField(_('born date'), default='1970-01-01')
    gender = models.CharField(_('gender'), max_length=1, choices=(
        ('M', _('Male')),
        ('F', _('Female')),
        ('', _('undefined')),
    ))
    last_donation_type = models.CharField(_('last donation'), max_length=1, blank=True, choices=donation_type)
    blood_type = models.CharField(_('blood type'), max_length=2, blank=True, null=True, choices=(
        ('O', 'O'),
        ('AB', 'AB'),
        ('A', 'A'),
        ('B', 'B'),
    ))
    blood_rh = models.CharField(_('blood rh'), max_length=1, blank=True, null=True, choices=(
        ('+', _('Positive')),
        ('-', _('Negative')),
        ('', _('undefined')),
    ))
    last_donation_date = models.DateField(_('last donation date'), default='1970-01-01', blank=True, null=True)
    suspension_date = models.DateField(_('suspension date'), blank=True, null=True)
    suspension_reason = models.CharField(_('suspension reason'), max_length=512, blank=True)
    phone = models.CharField(_('phone'), max_length=200, blank=True)
    email = models.CharField(_('email'), max_length=200, blank=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False)
    ordering = ['-created_at']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('donor')
        verbose_name_plural = _('donors')


class Donation(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name=_('donor'))
    done_at = models.DateTimeField(_('done at'), default=timezone.now)
    created_at = models.DateTimeField(_('created at'), default=timezone.now, editable=False)
    donation_type = models.CharField(_('donation type'), max_length=1, blank=True, choices=donation_type)
    ordering = ['-done_at']

    def done_at_pretty(self):
        return self.done_at.strftime('%Y-%m-%d')

    def __str__(self):
        return 'donation by {}'.format(self.donor.name)

    class Meta:
        verbose_name = _('donation')
        verbose_name_plural = _('donations')


class Reminder(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, verbose_name=_('donor'))
    sent_at = models.DateTimeField(_('done at'), default=timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name=_('created by'))
    ordering = ['-sent_at']

    def __str__(self):
        return 'reminder for ' + self.donor.name + ' at ' + self.sent_at.strftime('%d %B %Y')

    class Meta:
        verbose_name = _('reminder')
        verbose_name_plural = _('reminders')
