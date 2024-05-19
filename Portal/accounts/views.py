from django.shortcuts import render
from .models import User 
from django.contrib.auth.models import Group
from rest_framework.response import Response 
from rest_framework import generics, status
from .serializers import (MyTokenObtainPairSerializer,RegisterEmployeeSerializer ,UserCreateSerializer ,RegisterCompanySerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.none()  # No queryset needed for create-only views
    permission_classes = [AllowAny]  # Adjust permissions as needed
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data
        user = serializer.save()
        

class RegisterCompanyView(CreateAPIView):
    serializer_class = RegisterCompanySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        user = result['user']
        company = result['company']
        
        # Set the user's role to 'company'
        user.role = User.Role.COMPANY
        user.save()
        
        # Add the user to the 'Company' group
        try:
            group_object = Group.objects.get(name='Company')
        except Group.DoesNotExist:
            group_object = Group.objects.create(name='Company')
        
        user.groups.add(group_object)
        
        response_data = {
            'status': 'success',
            'message' : 'The user has been created successfully',
            'user': {
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'company': {
                'company_name': company.company_name,
                'location': company.location,
                'employee_count': company.employee_count,
                'field_work': company.field_work,
                'phone_number': company.phone_number,
            }
        }

        return Response(data = response_data, status=status.HTTP_201_CREATED)
 

class RegisterEmployeeView(generics.CreateAPIView):
   serializer_class = RegisterEmployeeSerializer
    
   def create(self, request,):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        user = result['user']
        employee = result['employee']
        
        user.role = User.Role.EMPLOYEE
        user.save()
        
        # Add the user to the 'Company' group
        try:
            group_object = Group.objects.get(name='Employee')
        except Group.DoesNotExist:
            group_object = Group.objects.create(name='Employee')
        
        user.groups.add(group_object)
        
        response_data = {
            'status': 'success',
            'user': user,
            'employee': employee
        }

        return Response(data = response_data, status=status.HTTP_201_CREATED)
         
## Login For all 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
## LogOut
class Logout(APIView):
    def get(self, request):
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return Response("User is not authenticated", status=HTTP_401_UNAUTHORIZED)

            # Delete user's authentication token (if applicable)
            # Replace 'auth_token' with the actual field name if using a token library
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()

            # Logout the user
            logout(request)

            return Response("User logged out successfully", status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors during logout
            return Response(f"Logout failed: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)