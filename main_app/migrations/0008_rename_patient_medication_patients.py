# Generated by Django 5.1.7 on 2025-03-13 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_patient_medications_medication_patient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medication',
            old_name='patient',
            new_name='patients',
        ),
    ]
