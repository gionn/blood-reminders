import logging
from datetime import timedelta

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from reminders.query import DonorQuerySet

from .forms import UploadFileForm
from .models import Donation, Donor, Reminder
from .upload_sif import parse_donations_file, parse_donors_file

logger = logging.getLogger(__name__)


class BloodTypeFilter(admin.SimpleListFilter):
    title = _('blood type')
    parameter_name = 'blood'

    def lookups(self, request, model_admin):
        return (
            ('O', _('O')),
            ('A', _('A')),
            ('B', _('B')),
            ('AB', _('AB')),
        )

    def queryset(self, request, queryset):
        donor_queryset = DonorQuerySet()
        if self.value():
            return donor_queryset.get_donors_with_blood_type(queryset, self.value())


class BloodRhFilter(admin.SimpleListFilter):
    title = _('blood rh')
    parameter_name = 'rh'

    def lookups(self, request, model_admin):
        return (
            ('+', _('Positive')),
            ('-', _('Negative')),
        )

    def queryset(self, request, queryset):
        donor_queryset = DonorQuerySet()
        if self.value():
            return donor_queryset.get_donors_with_blood_rh(queryset, self.value())


class NeedsReminderSentFilter(admin.SimpleListFilter):
    title = _('reminder needed')
    parameter_name = 'reminder'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Reminder to be sent')),
            ('false', _('Reminder not needed')),
        )

    def queryset(self, request, queryset):
        donor_queryset = DonorQuerySet()
        if self.value() == 'true':
            return donor_queryset.get_donors_with_reminders(queryset)
        if self.value() == 'false':
            return donor_queryset.get_donors_without_reminders(queryset)


class LastDonationFilter(admin.SimpleListFilter):
    title = _('last donation')
    parameter_name = 'last_donation_from'

    def lookups(self, request, model_admin):
        return (
            ('0', _('In the last year')),
            ('1', _('More than 1 year ago')),
            ('2', _('More than 2 years ago')),
            ('2+', _('More than 3 years')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(
                last_donation_date__gte=timezone.now() - timedelta(days=360)
            )
        if self.value() == '1':
            return queryset.filter(
                last_donation_date__lte=timezone.now() - timedelta(days=360),
                last_donation_date__gte=timezone.now() - timedelta(days=720)
            )
        if self.value() == '2':
            return queryset.filter(
                last_donation_date__lte=timezone.now() - timedelta(days=720),
                last_donation_date__gte=timezone.now() - timedelta(days=1080)
            )
        if self.value() == '2+':
            return queryset.filter(
                last_donation_date__lte=timezone.now() - timedelta(days=1080)
            )


class DonorAdmin(admin.ModelAdmin):
    list_filter = (
        NeedsReminderSentFilter,
        LastDonationFilter,
        BloodTypeFilter,
        BloodRhFilter,
    )
    search_fields = ['name', 'tax_code']
    ordering = ['-created_at']
    list_display = (
        'name', 'gender', 'last_donation_type', 'last_donation_date', 'whatsapp_send'
    )
    actions = ['create_reminder']
    view_on_site = False
    list_per_page = 20

    def whatsapp_send(self, obj):
        if obj.phone:
            return format_html('<a target=_blank href="https://api.whatsapp.com/send?phone={}"></a>', obj.phone)

    class Media:
        css = {
            "all": ("my_styles.css",)
        }

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload/', self.admin_site.admin_view(self.upload_donors), name='upload_donors')
        ]
        return my_urls + urls

    def upload_donors(self, request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                parse_donors_file(request.FILES['file'])
                return HttpResponseRedirect(reverse('admin:reminders_donor_changelist'))
        else:
            form = UploadFileForm()
        context = dict(
            self.admin_site.each_context(request),
        )
        context['form'] = form
        context['form_url'] = 'admin:upload_donors'
        context['title'] = 'Import donors CSV'
        return TemplateResponse(request, 'upload.html', context)

    def create_reminder(self, request, queryset):
        for donor in queryset:
            Reminder.objects.create(
                donor=donor,
                created_by=request.user
            )


class DonationAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-done_at']
    list_display = ('donor', 'done_at_pretty', 'donation_type')
    view_on_site = False
    list_per_page = 20

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload/', self.admin_site.admin_view(self.upload_donations), name='upload_donations')
        ]
        return my_urls + urls

    def upload_donations(self, request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                parse_donations_file(request.FILES['file'])
                return HttpResponseRedirect(reverse('admin:reminders_donation_changelist'))
        else:
            form = UploadFileForm()
        context = dict(
            self.admin_site.each_context(request),
        )
        context['form'] = form
        context['form_url'] = 'admin:upload_donations'
        context['title'] = 'Import donations CSV'
        return TemplateResponse(request, 'upload.html', context)


class ReminderAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-sent_at']
    view_on_site = False
    list_per_page = 20
    readonly_fields = ['created_by']


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.site_header = _('Blood donors management')
