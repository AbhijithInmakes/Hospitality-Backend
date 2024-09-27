from django.urls import path
from .views import AppointmentDetailView, CreateEPrescriptionView, DoctorCreateView, DoctorUpcomingAppointmentsView, EPrescriptionCreateView,MedicalHistoryCreateView, MedicalHistoryListCreateView,DoctorListView, PrescriptionUpdateView, PrescriptionView,RemoveMedicalHistory,DoctorDetail,DoctorDetailView,PrescriptionDeleteView

urlpatterns = [
    path('create-doctor/', DoctorCreateView.as_view(), name='create-doctor'),
    path('create-medicalhistory/',MedicalHistoryCreateView.as_view(),name='medical-history'),
    path('patients/<int:patient_id>/medical-history/', MedicalHistoryListCreateView.as_view(), name='medical-history'),
     path('doctors/<int:doctor_id>/appointments/', DoctorUpcomingAppointmentsView.as_view(), name='doctor-upcoming-appointments'),
      path('appointments/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
       path('prescriptions/create/', CreateEPrescriptionView.as_view(), name='create-prescription'),
       path('doctors/',DoctorListView.as_view()),
       path('medical-history/<int:medical_history_id>/remove/',RemoveMedicalHistory.as_view()),
         path('doctor-detail/', DoctorDetail.as_view(), name='doctor-detail'),
         path('doctor-detail-view/', DoctorDetailView.as_view(), name='doctor-detail-view'),
         path('create-prescription/<int:patient_id>/', EPrescriptionCreateView.as_view(), name='create_prescription'),
        path('prescription/update/<int:prescription_id>/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescription/<int:patient_id>/', PrescriptionView.as_view(), name='prescription_detail'),
    path('prescription/<int:prescription_id>/remove',PrescriptionDeleteView.as_view() , name='prescription_delete'),


]
