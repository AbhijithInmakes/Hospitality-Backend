from django.db import models
from user_management.models import User
from docter_management.models import Doctor

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    name=models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField(null=True, blank=True)
    treatment_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Medical History of {self.patient.user.first_name} {self.patient.user.last_name}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[(0, 'Pending'), (1, 'Paid')])
    billing_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient.user.first_name} {self.patient.user.last_name} - {self.amount} USD"
    

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.IntegerField( choices=[(0, 'Scheduled'), (1, 'Cancelled'), (2, 'Completed')])

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} on {self.appointment_date}"
    



