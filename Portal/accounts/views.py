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

class RegisterCompanyView(CreateAPIView):
    serializer_class = RegisterCompanySerializer
    
    def perform_create(self, serializer):
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
            'user': user,
            'company':company
        }

        return Response(data = response_data, status=status.HTTP_201_CREATED)
 

class RegisterEmployeeView(generics.CreateAPIView):
    """View for registering an employee."""
    queryset = User.objects.none()  # Assuming we don't need queryset here
    permission_classes = [AllowAny]
    serializer_class = RegisterEmployeeSerializer

    def perform_create(self, serializer):
        inst = serializer.save(role=User.Role.EMPLOYEE)
        
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.none()  # No queryset needed for create-only views
    permission_classes = [AllowAny]  # Adjust permissions as needed
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data
        user = serializer.save()
        
        try:
                group_object = Group.objects.get(name='Company')  # Attempt to retrieve the group
        except Group.DoesNotExist:
            # Create the group if it doesn't exist
            group_object = Group.objects.create(name='Company')
            
        user.groups.add(group_object)
        
        return Response(status.HTTP_201_CREATED)
    

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