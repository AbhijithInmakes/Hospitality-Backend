from rest_framework import serializers
from .models import MedicalHistory, Patient
from datetime import date, datetime
from docter_management.serializers import DoctorSerializer

class PatientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'address', 'phone_number','name','id']

    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    
   
    
from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer() 
    patient=PatientSerializer()

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'status','patient','id']

class PatientListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Patient
        fields='__all__'

class PatientUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Patient
        fields=['name','date_of_birth','gender','address','phone_number']

    def update(self, instance, validated_data):

        instance.name=validated_data['name']
       
        instance.date_of_birth=validated_data['date_of_birth']
        instance.gender=validated_data['gender']
        instance.address=validated_data['address']
        instance.phone_number=validated_data['phone_number']
        instance.save()
        return instance
    


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['patient', 'diagnosis', 'medications', 'allergies', 'treatment_history']
       
