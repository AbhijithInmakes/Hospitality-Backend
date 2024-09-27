from django.db import models
from user_management.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    specialty = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class EPrescription(models.Model):
    doctor = models.ForeignKey('docter_management.Doctor', on_delete=models.CASCADE, related_name='prescriptions')  # Lazy reference
    patient = models.ForeignKey('patient_management.Patient', on_delete=models.CASCADE, related_name='prescriptions')  # Lazy reference
    medication = models.TextField()
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.user.first_name} by Dr. {self.doctor.user.last_name}"
