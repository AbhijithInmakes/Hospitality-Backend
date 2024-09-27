from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from patient_management.models import Appointment
from patient_management.serializers import AppointmentSerializer
from patient_management.models import MedicalHistory, Patient
from .models import Doctor, EPrescription
from .serializers import DoctorSerializer, MedicalHistorySerializer, PrescriptionUpdateSerializer
from user_management.models import User
from docter_management.models import Doctor
from rest_framework import generics
from patient_management.permission import IsAdminUser,IsDocterUser
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

class DoctorCreateView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        user_id=request.data.get("user_id")
        try:
            user=User.objects.get(id=user_id,user_type=2)
           
           
            doctor=Doctor.objects.create(specialty=request.data.get('specialty'),
                                             license_number=request.data.get('license_number'),
                                              user=user)
            return Response({"message": "Doctor created successfully"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message":"User is not found"}, status=status.HTTP_400_BAD_REQUEST)

class MedicalHistoryCreateView(APIView):
    permission_classes = [IsDocterUser]  

    def post(self, request, *args, **kwargs):
        patient_id=request.data.get('patient_id')
        try:

            patient = Patient.objects.get(id=patient_id)
            serializer = MedicalHistorySerializer(data=request.data)
            
            if serializer.is_valid():
                
                medical_history = serializer.save(patient=patient)  
                return Response({"message": "Medical history created successfully", 
                                "data": serializer.data}, 
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
             return Response({"message":"Patient doesnot exist"}, status=status.HTTP_400_BAD_REQUEST)
        
class MedicalHistoryListCreateView(generics.ListAPIView):
    serializer_class = MedicalHistorySerializer
    

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return MedicalHistory.objects.filter(patient__id=patient_id)
    

class RemoveMedicalHistory(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        medical_history_id=kwargs.get('medical_history_id')
        medical_history=MedicalHistory.objects.get(id=medical_history_id)
        medical_history.delete()

        return Response({"message":"Removed Successfully"},status=status.HTTP_200_OK)
    

class DoctorUpcomingAppointmentsView(APIView):
    
    def get(self, request, doctor_id):
       
        current_time = now()
        
       
        appointments = Appointment.objects.filter(
            doctor__id=doctor_id, 
            appointment_date__gte=current_time, 
            status=0 
        ).order_by('appointment_date')
        serializer = AppointmentSerializer(appointments, many=True)
        
       
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AppointmentDetailView(generics.RetrieveAPIView):

    def retrieve(self, request,appointment_id, *args, **kwargs):
       
        try:
            appointment =  Appointment.objects.get(id=appointment_id)
            serializer=AppointmentSerializer(appointment)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"message":"Appointment doesnt exist"},status=status.HTTP_400_BAD_REQUEST)
        
class CreateEPrescriptionView(APIView):
    permission_classes=[IsDocterUser]

    def post(self, request, *args, **kwargs):
    
        doctor_id = Doctor.objects.get(user=request.user).id
        patient_id = request.data.get('patient_id')
        medication = request.data.get('medication')
        dosage = request.data.get('dosage')
        instructions = request.data.get('instructions')

        
        if not (doctor_id and patient_id and medication and dosage and instructions):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
          
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

       
        prescription = EPrescription.objects.create(
            doctor=doctor,
            patient=patient,
            medication=medication,
            dosage=dosage,
            instructions=instructions,
            date_prescribed=now() 
        )

        return Response({"message": "Prescription created successfully", "prescription_id": prescription.id}, status=status.HTTP_201_CREATED)
    
class DoctorListView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        doctors=Doctor.objects.all()
        serializer=DoctorSerializer(doctors,many=True)
        return Response(serializer.data)
    
class DoctorDetail(generics.GenericAPIView):
    permission_classes = [IsDocterUser]

    def post(self, request, *args, **kwargs):
       
        license_number = request.data.get("license_number")
        specialty = request.data.get("specialty")
        user = request.user 
       
       
        doctor, created = Doctor.objects.update_or_create(
            user=user, 
            defaults={
                'license_number': license_number,
                'specialty': specialty,
            }
        )

      
        if created:
            message = "Doctor profile created successfully."
            response_status = status.HTTP_201_CREATED
        else:
            message = "Doctor profile updated successfully."
            response_status = status.HTTP_200_OK

        return Response({
            'message': message,
            'doctor': {
                
                'license_number': doctor.license_number,
                'specialty': doctor.specialty,
            }
        }, status=response_status)
    

class DoctorDetailView(generics.RetrieveAPIView):
    permission_classes=[IsDocterUser]
    serializer_class=DoctorSerializer

    def get(self, request, *args, **kwargs):
        try:
            doctor=Doctor.objects.get(user=request.user.id)
            serializer=DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({"message":"Doctor dara doesnt exist"},status=status.HTTP_400_BAD_REQUEST)
        
class EPrescriptionCreateView(generics.CreateAPIView):
    permission_classes=[IsDocterUser]

    def post(self, request, *args, **kwargs):
       
        try:
            doctor_id =request.user.id
            patient_id = kwargs.get('patient_id')
            medication = request.data.get('medication')
            dosage = request.data.get('dosage')
            instructions = request.data.get('instructions')

           
            if not all([doctor_id, patient_id, medication, dosage, instructions]):
                return Response({"message": "Missing required fields"}, status=400)
            
           
            try:
                doctor = Doctor.objects.get(user=doctor_id)
                patient = Patient.objects.get(id=patient_id)
            except ObjectDoesNotExist:
                return Response({"message": "Doctor or Patient not found"}, status=404)
            
            prescription = EPrescription.objects.create(
                doctor=doctor,
                patient=patient,
                medication=medication,
                dosage=dosage,
                instructions=instructions
            )

           
            return Response({
                "message": "Prescription created successfully",
                "prescription_id": prescription.id
            }, status=201)
        
        except Exception as e:
            return Response({"message": str(e)}, status=500)       
        

class PrescriptionUpdateView(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        
        try:
            prescription_id = kwargs.get('prescription_id')
            patient=EPrescription.objects.get(id=prescription_id)

            
            serializer=PrescriptionUpdateSerializer(patient,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response({"message":"Prescription details update successfully","data":serializer.data},status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message":"Prescription doesnt exist"},status=status.HTTP_400_BAD_REQUEST)
        

class PrescriptionView(generics.ListAPIView):
    queryset=EPrescription.objects.all()
    serializer_class=PrescriptionUpdateSerializer
    lookup_field='patient_id'

class PrescriptionDeleteView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
       
        prescription_id=kwargs.get('prescription_id')
        prescription=EPrescription.objects.get(id=prescription_id)
        prescription.delete()
        return Response({"message":"Prescription deleted successfully"},status=status.HTTP_200_OK)
   