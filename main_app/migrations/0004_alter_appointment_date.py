# Generated by Django 5.1.7 on 2025-03-12 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_appointments_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(verbose_name='Appointment Date'),
        ),
    ]
