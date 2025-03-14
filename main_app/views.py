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
    # patients = Patient.objects.all()
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
        #  this can probably be done to other things lkke meds and apt
        return super().form_valid(form)


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    fields = '__all__' 


class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = '/patients/'

@login_required
# change this to createview and pass in form how?  or jus change name 
def add_appointment(request):
    # form = AppointmentForm()
    form = AppointmentForm(request.POST)
    if form.is_valid():
        new_appointment = form.save(commit=False)
        # assign the cat_id to the form for the cat_id column in psql
        # new_appointment.patient_id = patient_id --- appointment.pateint_id?
        new_appointment.save()
        return redirect('appointment-index')
    return render(request, 'main_app/appointment_form.html', {'form': form})

   
  
class AppointmentList(LoginRequiredMixin, ListView):
    model = Appointment


class AppointmentDetail(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    # template_name="main_app/appointment_form.html"
    model = Appointment 
    fields = ['date', 'time', 'address', 'notes']

    def form_valid(self, form):
        return super().form_valid(form)

   
class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment 
    success_url = '/appointments/'


# def add_medication(request, patient_id):
#     form = MedicationForm(request.POST)
#     if form.is_valid():
#         new_medication = form.save(commit=False)
#         new_medication.patient_id = patient_id
#         new_medication.save()
#     # print(form)
#     # return redirect('add-medication', patient_id = patient_id)
#     return render(request, 'main_app/medication_form.html', {'form': form, 'patient_id': patient_id})

class MedicationCreate(LoginRequiredMixin, CreateView):
    model = Medication
    fields = ['name', 'dosage', 'pill_amount', 'times_per_day', 'time_of_day', 'perscribed_by', 'notes', 'patient']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     patient_id = self.kwargs['patient_id']
    #     context['patient_id'] = patient_id
    #     return context
    # pk_url_kwarg = 'medication_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.kwargs['patient_id']
        # medication_id = self.kwargs['medication_id']
        context['patient_id'] = patient_id
        # context['medication_id'] = medication_id
        return context
        
    def form_valid(self, form):
        # form.instance.patient = self.request.patient
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('patient-details', kwargs={'patient_id': self.kwargs['patient_id']})
    # def get_success_url(self):
    #     return reverse('medication-details', kwargs={'patient_id': self.kwargs['patient_id'], , 'medication_id': self.kwargs['medication_id']})
    #  does this work as medication-details ?????? 
    # ther is no medication id in the url for the method to grab! 


@login_required
def medication_details(request, patient_id, medication_id):
    patient = Patient.objects.get(id=patient_id)
    medication = Medication.objects.get(id=medication_id)
    return render(request, 'main_app/medication_detail.html', {'patient': patient, 'medication': medication})


class MedicationUpdate(LoginRequiredMixin, UpdateView):
    model = Medication 
    fields = ['dosage', 'pill_amount', 'time_of_day', 'notes']

# normally, update uses pk so this tells the cbv that the pk is medication_id
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