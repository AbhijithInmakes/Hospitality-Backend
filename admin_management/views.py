from django.shortcuts import render
from rest_framework import viewsets
from .models import Facility
from .serializers import FacilitySerializer
from patient_management.permission import IsAdminUser

class FacilityViewSet(viewsets.ModelViewSet):
    
    permission_classes=[IsAdminUser]
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


