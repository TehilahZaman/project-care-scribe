from django import forms 
from .models import Appointment, Medication

class AppointmentForm(forms.ModelForm):
    class Meta: 
        model = Appointment 
        fields = ['patient', 'date', 'time', 'dr_name', 'appointment_type', 'address', 'notes']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            )
        }


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'pill_amount', 'times_per_day', 'need_to_refill', 'time_of_day', 'perscribed_by', 'notes' ]