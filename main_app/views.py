from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Patient, Appointment, Medication
from .forms import AppointmentForm, MedicationForm
from django import forms
import calendar
from datetime import date


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient-index')
        else:
            error_message = 'Invalid sign up, pleae try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: return render(request, 'signup.html',{'form': form, 'error_message': error_message})


class home(LoginView):
    template_name= 'home.html'

@login_required
def patient_index(request):

    patients = Patient.objects.filter(user=request.user)
    return render(request, 'patients/index.html', {'patients': patients})

@login_required
def patient_details(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    appointments = Appointment.objects.all()
    medications = Medication.objects.all()
    return render(request, 'patients/details.html', {'patient': patient, 'appointments': appointments, 'medications': medications})


class PatientCreate(LoginRequiredMixin, CreateView):
    model = Patient
    fields = ['name', 'age', 'diagnosis', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    fields = ['name', 'age', 'diagnosis', 'notes']
    

class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = '/patients/'

@login_required
def add_appointment(request):
    form = AppointmentForm(request.POST)
    if form.is_valid():
        new_appointment = form.save(commit=False)
        new_appointment.user_id = request.user.id
        new_appointment.save()
        return redirect('calendar-view')
    return render(request, 'main_app/appointment_form.html', {'form': form})

  
class AppointmentList(LoginRequiredMixin, ListView):
    model = Appointment


def calendar_view(request, year=None, month=None):
    appointments_list = Appointment.objects.filter(user=request.user)
    
    if not year or not month:
        today = date.today()
        year, month = today.year, today.month

# generate all the day in any month in a list 
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(year, month))
# filter the appointment by year and month 
    appointments = appointments_list.filter( date__year=year, date__month=month)

    days_with_appts = []
    for day in month_days:
        if day == 0:
            days_with_appts.append((0, []))
        else:
            appt_list = [appt for appt in appointments if appt.date.day == day]
            days_with_appts.append((day, appt_list))


#  send all information to html template 
    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "days": month_days,
        "appts": days_with_appts,
        "appointments_list": appointments_list,
    }
    return render(request, 'appointments/calendar.html', context)


class AppointmentDetail(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    model = Appointment 
    fields = ['date', 'time', 'address', 'notes']

    def form_valid(self, form):
        return super().form_valid(form)

   
class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment 
    success_url = '/appointments/'


class MedicationCreate(LoginRequiredMixin, CreateView):
    model = Medication
    fields = ['name', 'dosage', 'pill_amount', 'times_per_day', 'time_of_day', 'perscribed_by', 'patient', 'notes',]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs['patient_id']
        
        context['patient_id'] = patient_id
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('patient-details', kwargs={'patient_id': self.kwargs['patient_id']})



@login_required
def medication_details(request, patient_id, medication_id):
    patient = Patient.objects.get(id=patient_id)
    medication = Medication.objects.get(id=medication_id)
    return render(request, 'main_app/medication_detail.html', {'patient': patient, 'medication': medication})


class MedicationUpdate(LoginRequiredMixin, UpdateView):
    model = Medication 
    fields = ['dosage', 'pill_amount', 'time_of_day', 'notes']

    pk_url_kwarg = 'medication_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs['patient_id']
        medication_id = self.kwargs['medication_id']
        context['patient_id'] = patient_id
        context['medication_id'] = medication_id
        return context

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('medication-details', kwargs={'patient_id': self.kwargs['patient_id'], 'medication_id': self.kwargs['medication_id']})

class MedicationDelete(LoginRequiredMixin, DeleteView):
    model = Medication 

    pk_url_kwarg = 'medication_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs['patient_id']
        context['patient_id'] = patient_id
        return context
    
    def get_success_url(self):
        return reverse('patient-details', kwargs={'patient_id': self.kwargs['patient_id']})