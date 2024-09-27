from django.urls import path
from .views import MedicalHistoryCreateView, PatientCreateView,AppointmentCreateView,PatientMedicalHistoryListView,PatientDetailView,PatientListView,PatientDeleteView,PatientUpdateView,AppointmentListView,AllAppointmentView,AppointmentStatusUpdateView,AppointmentDelete,AllPatientListView,DoctorAppointmentView

urlpatterns = [
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('create-appointment/', AppointmentCreateView.as_view(), name='create-appointment'),
     path('medical-history/', PatientMedicalHistoryListView.as_view(), name='patient-medical-history'),
     path('patients/detail/', PatientDetailView.as_view(), name='patient-detail'),
     path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:patient_id>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
     path('patients/<int:patient_id>/update/', PatientUpdateView.as_view(), name='patient-update'),
      path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
      path('all-appointments/', AllAppointmentView.as_view(), name='appointment-all-list'),
      path('appointments/<int:appointment_id>/update', AppointmentStatusUpdateView.as_view(), name='appointment-status-update'),
      path('appointments/<int:appointment_id>/delete', AppointmentDelete.as_view(), name='appointment-delete'),
      path('all-patients/', AllPatientListView.as_view(), name='patient-list'),
       path('medical-history/<int:patient_id>/create/', MedicalHistoryCreateView.as_view(), name='medical-history-create'),
       path('doctor-appointments/', DoctorAppointmentView.as_view(), name='doctor-appointments'),


     



]
