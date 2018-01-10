from django.contrib import admin

from .models import Donor
from .models import Donation
from .models import Reminder

admin.site.register(Donor)
admin.site.register(Donation)
admin.site.register(Reminder)
