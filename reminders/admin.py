import logging

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from reminders.query import DonorQuerySet

from .forms import UploadFileForm
from .models import Donation, Donor, Reminder
from .upload import handle_uploaded_donations_file, handle_uploaded_donors_file

logger = logging.getLogger(__name__)

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


class DonorAdmin(admin.ModelAdmin):
    list_filter = (NeedsReminderSentFilter,)
    search_fields = ['name','tax_code']
    ordering = ['-created_at']
    list_display = ('name', 'gender', 'last_donation_type', 'last_donation_date', 'whatsapp_send')
    actions = ['create_reminder']
    view_on_site = False

    def whatsapp_send(self, obj):
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
                handle_uploaded_donors_file(request.FILES['file'])
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
                donor = donor,
                created_by = request.user
            )


class DonationAdmin(admin.ModelAdmin):
    search_fields = ['donor__name']
    autocomplete_fields = ['donor']
    ordering = ['-done_at']
    list_display = ('donor', 'done_at_pretty', 'donation_type')
    view_on_site = False

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
                handle_uploaded_donations_file(request.FILES['file'])
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
    readonly_fields = ['created_by']


admin.site.register(Donor, DonorAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.site_header = 'Blood donors reminders system'
