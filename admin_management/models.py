from django.db import models
from patient_management.models import Appointment
from user_management.models import User

class Facility(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AppointmentManagement(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[(0, 'Scheduled'), (1, 'Cancelled'), (2, 'Completed')])
   

    def __str__(self):
        return f"Managed by {self.admin.user.first_name} {self.admin.user.last_name}"

