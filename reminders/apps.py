from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RemindersConfig(AppConfig):
    name = 'reminders'
    verbose_name = _('donors management')
