from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User
    

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diagnosis = models.CharField(max_length=150)
    notes = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('patient-details', kwargs={'patient_id': self.id})

    def __str__(self):
        return self.name


class Appointment(models.Model):
    dr_name = models.CharField(max_length=100)
    appointment_type = models.CharField(max_length=100)
    date = models.DateField('Appointment Date')
    time = models.TimeField()
    address = models.CharField(max_length=100)
    notes = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('appointment-details', kwargs={"pk": self.id})

    def __str__(self):
        return f"appointment for {self.patient} on {self.date}"
    
TIME_OF_DAY = (
    ("M", "Morning"),
    ("A", "Afternoon"),
    ("E", "Evening"),
    )

class Medication(models.Model):
    name = models.CharField(max_length=50)
    dosage = models.DecimalField(max_digits=10, decimal_places=3)
    pill_amount = models.DecimalField(max_digits=10, decimal_places=3)
    times_per_day = models.IntegerField()
    need_to_refill = models.BooleanField(default=False)
    time_of_day = models.CharField( max_length=1, choices=TIME_OF_DAY, default=TIME_OF_DAY[0][0])
    perscribed_by = models.CharField(max_length=50)
    notes = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} for {self.patient}"
    
    def get_absolute_url(self):
        return reverse('medication-details', kwargs={'patient_id': self.patient, 'medication_id': self.id})
    