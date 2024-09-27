from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from patient_management.permission import IsAdminUser
from .serializers import UserListSerializer, UserSignupSerializer, UserUpdateSerializer
from user_management.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupView(APIView):
    
    def post(self, request, *args, **kwargs):
        
        email=request.data.get("email")
        
        try:
            user=User.objects.get(email=email)
            return Response({"message":"user is already exist"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:

                serializer = UserSignupSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    return Response({"message": "User created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
           
    

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

    
        user = authenticate(email=email, password=password)


        if user is not None:
            
            refresh = RefreshToken.for_user(user)
            access_token=refresh.access_token
            access_token['user_type'] = user.user_type
            access_token = str(access_token)
            
            return Response({
                'refresh': str(refresh),
                'access': access_token,
                'user_type':user.user_type,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        else:
            return  Response({"message":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)
        

class UserUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]  

    def put(self, request, *args, **kwargs):
        try:
            user=User.objects.get(id=request.data.get('user_id')) 
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()  
                return Response({
                    "message": "User updated successfully", 
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message":"User does not exist"},status=status.HTTP_400_BAD_REQUEST)
        

class UserStatusUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]  

    def put(self, request, *args, **kwargs):
        
        try:
            user=User.objects.get(id=kwargs['user_id']) 
            user.is_active = False if user.is_active else True

            user.save()
            return Response({"message":"User status updated"},status=status.HTTP_200_OK)
            
           
        except User.DoesNotExist:
            return Response({"message":"User does not exist"},status=status.HTTP_400_BAD_REQUEST)
        
class UserListView(generics.ListAPIView):
    serializer_class=UserListSerializer

    def get(self, request, *args, **kwargs):
       users = User.objects.exclude(user_type=2)
       seriliazer=self.get_serializer(users,many=True)

       return Response(seriliazer.data)
        

