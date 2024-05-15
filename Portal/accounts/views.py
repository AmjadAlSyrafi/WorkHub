from django.shortcuts import render
from .models import User
from .serializers import (MyTokenObtainPairSerializer,RegisterEmployeeSerializer ,RegisterCompanyView )
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# Create your views here.


class RegisterEmployeeView(generics.CreateAPIView):
    """View for registering an employee."""
    queryset = User.objects.none()  # Assuming we don't need queryset here
    permission_classes = [AllowAny]
    serializer_class = RegisterEmployeeSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.EMPLOYEE)

class RegisterCompanyView(generics.CreateAPIView):
    """View for registering an employee."""
    queryset = User.objects.none()  # Assuming we don't need queryset here
    permission_classes = [AllowAny]
    serializer_class = RegisterCompanySerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.Company)

## Login For all 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
## LogOut
class Logout(APIView):
    def get(self, request):
        # Delete user's authentication token
        request.user.auth_token.delete()
        # Logout the user
        auth.logout(request)
        return Response("User logged out successfully", status=status.HTTP_200_OK)