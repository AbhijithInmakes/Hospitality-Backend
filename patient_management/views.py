from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from docter_management.models import Doctor
from docter_management.serializers import MedicalHistorySerializer
from .serializers import AppointmentSerializer, PatientListSerializer, PatientSerializer, PatientUpdateSerializer
from datetime import date,datetime
from django.utils import timezone
from patient_management.permission import IsDocterUser, IsPatientUser,IsAdminUser
from patient_management.models import Appointment, MedicalHistory, Patient
from docter_management.models import Doctor


class PatientCreateView(generics.CreateAPIView):
    permission_classes = [IsPatientUser]
    
    def post(self, request, *args, **kwargs):
       
        date_of_birth=request.data.get("date_of_birth")
        date_of_birth_str = request.data.get("date_of_birth")
        name=request.data.get('name')
        
    
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"message": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        if date_of_birth > date.today():
            return Response({"message":"Date of birth cannot be future"},status=status.HTTP_400_BAD_REQUEST)
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient=Patient.objects.create(date_of_birth=date_of_birth,
                                           name=name,
                                           gender=request.data.get("gender"),
                                           address=request.data.get("address"),
                                           phone_number=request.data.get("phone_number"),
                                           user=request.user
                                           )
            
            return Response({"message": "Patient created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AppointmentCreateView(APIView):
    permission_classes=[IsPatientUser]
    
    def post(self, request, *args, **kwargs):
         
        
            doctor_id = request.data.get("doctor_id")
            try:
                doctor=Doctor.objects.get(id=doctor_id)
                appointment_date_str = request.data.get('appointment_date')

        
                try:
                    appointment_date = timezone.datetime.fromisoformat(appointment_date_str)
                except ValueError:
                    return Response({"message": "Invalid date format. Use ISO 8601."},
                                    status=status.HTTP_400_BAD_REQUEST)


                if appointment_date < timezone.now():
                    return Response({"message": "Appointment date cannot be in the past."}, 
                                    status=status.HTTP_400_BAD_REQUEST)

                existing_appointment = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=appointment_date,
                    status=0
                ).exists()

                if existing_appointment:
                    return Response({"message": "Doctor already has an appointment at this time."}, 
                                    status=status.HTTP_400_BAD_REQUEST)

                patient=Patient.objects.get(user=request.user.id)
                appointment = Appointment.objects.create(doctor=doctor,patient=patient,appointment_date=appointment_date,status=0)
                return Response({"message": "Appointment created successfully","data": AppointmentSerializer(appointment).data}, 
                                status=status.HTTP_201_CREATED)
            except Doctor.DoesNotExist:
                return Response({"message": "Doctor is not found"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            

class PatientMedicalHistoryListView(APIView):
    permission_classes = [IsPatientUser]  

    def get(self, request,*args, **kwargs):
        try:
            
            patient = Patient.objects.get(user=request.user.id)
            
            medical_histories = MedicalHistory.objects.filter(patient=patient)
           
            serializer = MedicalHistorySerializer(medical_histories, many=True)
            return Response(
                serializer.data
            , status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message": "Patient does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
class AppointmentStatusUpdateView(generics.UpdateAPIView):
    permission_classes=[IsAdminUser]

    def put(self, request, *args, **kwargs):
        appointment_id=kwargs.get('appointment_id')
        statuz=request.data.get("status")
        
        try:

            appointment=Appointment.objects.get(id=appointment_id)
            appointment.status=statuz
            appointment.save()
            return Response({"message":"Appointment status update successfully"},status=status.HTTP_200_OK)
        
        except Appointment.DoesNotExist:
            return Response({"message":"Appointment does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
class AppointmentDelete(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        appointment_id=kwargs.get('appointment_id')
        appointment=Appointment.objects.get(id=appointment_id)
        appointment.delete()
        return Response({"message":"Deleted Successfully"},status=status.HTTP_200_OK)
    
class PatientDetailView(generics.ListAPIView):
    permission_classes=[IsPatientUser]
    serializer_class = PatientSerializer
    

    def get_queryset(self):

        return Patient.objects.filter(user=self.request.user)
    
class AllPatientListView(generics.ListAPIView):
    serializer_class=PatientSerializer

    def get(self, request, *args, **kwargs):
        patients=Patient.objects.all()
        serializer=PatientSerializer(patients,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class PatientDeleteView(generics.DestroyAPIView):
    def delete(self, request,patient_id, *args, **kwargs):
        try:
            patient=Patient.objects.get(id=patient_id)
            patient.delete()
        except Patient.DoesNotExist:
            return Response({"message":"Deleted successfully"},status=status.HTTP_400_BAD_REQUEST)

        return super().delete(request, *args, **kwargs)

class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [IsPatientUser]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class PatientUpdateView(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        
        try:
            patient_id = kwargs.get('patient_id')
            patient=Patient.objects.get(id=patient_id)
            request.data['date_of_birth'] = datetime.strptime(request.data.get("date_of_birth"), "%Y-%m-%d").date()
            
            serializer=PatientUpdateSerializer(patient,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response({"message":"Patient details update successfully","data":serializer.data},status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"message":"Patient doesnt exist"},status=status.HTTP_400_BAD_REQUEST)
        

class AppointmentListView(generics.ListAPIView):
    permission_classes = [IsPatientUser]
    serializer_class = AppointmentSerializer  

    def get_queryset(self):
        patient = Patient.objects.get(user=self.request.user.id)
        return Appointment.objects.filter(patient=patient.id)

    def get(self, request, *args, **kwargs):
    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)  
        return Response(serializer.data)
    
class DoctorAppointmentView(generics.ListAPIView):
    permission_classes = [IsDocterUser]
    serializer_class = AppointmentSerializer  

    def get_queryset(self):
        
        try:

            doctor = Doctor.objects.get(user=self.request.user.id)
            return Appointment.objects.filter(doctor=doctor.id)
        except Doctor.DoesNotExist:
            return Response([])

    def get(self, request, *args, **kwargs):
    
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)  
        return Response(serializer.data)
    
class AllAppointmentView(generics.ListAPIView):
    serializer_class=AppointmentSerializer

    def get_queryset(self):
        
        return Appointment.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        serializer=self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    

class MedicalHistoryCreateView(APIView):
    def post(self, request, *args, **kwargs):
       
        patient_id = kwargs.get('patient_id')
        diagnosis = request.data.get('diagnosis')
        medications = request.data.get('medications')
        allergies = request.data.get('allergies', '')  
        treatment_history = request.data.get('treatment_history')
        
 
        if not patient_id or not diagnosis or not medications or not treatment_history:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            patient = Patient.objects.get(id=patient_id)

            
            medical_history = MedicalHistory.objects.create(
                patient=patient,
                diagnosis=diagnosis,
                medications=medications,
                allergies=allergies,
                treatment_history=treatment_history
            )
            
            
            response_data = {
                "id": medical_history.id,
                "patient": medical_history.patient.id,
                "diagnosis": medical_history.diagnosis,
                "medications": medical_history.medications,
                "allergies": medical_history.allergies,
                "treatment_history": medical_history.treatment_history
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Patient.DoesNotExist:
            return Response({"message": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)


       
    
    
        

      

