from rest_framework import serializers
from .models import Doctor, EPrescription
from patient_management.models import MedicalHistory

class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['specialty', 'license_number','name','id'] 

    def get_name(self, obj):
        return f"Dr. {obj.user.username}"
    


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'medications', 'allergies', 'treatment_history','created_at','id']


class PrescriptionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model=EPrescription
        fields=['medication','dosage','instructions','id','created_at']

    def update(self, instance, validated_data):

        instance.medication=validated_data['medication']
        instance.dosage=validated_data['dosage']
        instance.instructions=validated_data['instructions']
        instance.save()
        return instance  
