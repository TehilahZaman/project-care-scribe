# Generated by Django 5.1.7 on 2025-03-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_patient_aide_patient_medications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='medications',
        ),
        migrations.AddField(
            model_name='medication',
            name='patient',
            field=models.ManyToManyField(to='main_app.patient'),
        ),
    ]
