# Generated by Django 2.2.10 on 2020-03-28 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0002_auto_20180211_1003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'verbose_name': 'donation', 'verbose_name_plural': 'donations'},
        ),
        migrations.AlterModelOptions(
            name='donor',
            options={'verbose_name': 'donor', 'verbose_name_plural': 'donors'},
        ),
        migrations.AlterModelOptions(
            name='reminder',
            options={'verbose_name': 'reminder', 'verbose_name_plural': 'reminders'},
        ),
        migrations.AlterField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_type',
            field=models.CharField(blank=True, choices=[('B', 'Blood'), ('P', 'Plasma'), ('M', 'Multicomponent')], max_length=1, verbose_name='donation type'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='done_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='done at'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reminders.Donor', verbose_name='donor'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='blood_rh',
            field=models.CharField(blank=True, choices=[('+', 'Positive'), ('-', 'Negative'), ('', 'undefined')], max_length=1, null=True, verbose_name='blood rh'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='blood_type',
            field=models.CharField(blank=True, choices=[('O', 'O'), ('AB', 'AB'), ('A', 'A'), ('B', 'B')], max_length=2, null=True, verbose_name='blood type'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='born_date',
            field=models.DateField(default='1970-01-01', verbose_name='born date'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='email',
            field=models.CharField(blank=True, max_length=200, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('', 'undefined')], max_length=1, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='last_donation_date',
            field=models.DateField(blank=True, default='1970-01-01', null=True, verbose_name='last donation date'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='last_donation_type',
            field=models.CharField(blank=True, choices=[('B', 'Blood'), ('P', 'Plasma'), ('M', 'Multicomponent')], max_length=1, verbose_name='last donation'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='phone',
            field=models.CharField(blank=True, max_length=200, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='suspension_date',
            field=models.DateField(blank=True, null=True, verbose_name='suspension date'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='suspension_reason',
            field=models.CharField(blank=True, max_length=512, verbose_name='suspension reason'),
        ),
        migrations.AlterField(
            model_name='donor',
            name='tax_code',
            field=models.CharField(max_length=16, unique=True, verbose_name='tax code'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reminders.Donor', verbose_name='donor'),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='sent_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='done at'),
        ),
    ]