from django.urls import path

from . import views 

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.home.as_view(), name='home'), 
    path('patients/', views.patient_index, name='patient-index'),
    path('patients/<int:patient_id>/', views.patient_details, name='patient-details'),
    path('patients/create/', views.PatientCreate.as_view(), name="patient-create"),
    path('patient/<int:pk>/update', views.PatientUpdate.as_view(), name="patient-update"),
    path('patient/<int:pk>/delete', views.PatientDelete.as_view(), name='patient-delete'),
    path('appointments/add-appointment', views.add_appointment, name='add-appointment'),
    path('appointments/', views.AppointmentList.as_view(), name='appointment-index'),
    path('calendar/', views.calendar_view, name='calendar-view'),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view(), name='appointment-details'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdate.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDelete.as_view(), name='appointment-delete'),
     path('patients/<int:patient_id>/medications/add-medication', views.MedicationCreate.as_view(), name='add-medication'),
    path('patients/<int:patient_id>/medications/<int:medication_id>/medication/', views.medication_details, name='medication-details'),
    path('patients/<int:patient_id>/medications/<int:medication_id>/medication/update', views.MedicationUpdate.as_view(), name='medication-update'),
    path('patients/<int:patient_id>/medications/<int:medication_id>/medication/delete', views.MedicationDelete.as_view(), name='medication-delete'),

 ]
