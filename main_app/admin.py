from django.contrib import admin

from .models import Patient, Appointment, Medication
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Medication)
