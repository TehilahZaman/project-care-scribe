# Generated by Django 5.1.7 on 2025-03-12 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_appointments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Appointments',
            new_name='Appointment',
        ),
    ]
