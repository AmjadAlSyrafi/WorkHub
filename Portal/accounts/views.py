from django.shortcuts import render
from .models import User 
from django.contrib.auth.models import Group
from rest_framework.response import Response 
from rest_framework import generics, status
from .serializers import (MyTokenObtainPairSerializer,RegisterEmployeeSerializer ,UserCreateSerializer,OTPVerificationSerializer ,CustomPasswordResetSerializer,RegisterCompanySerializer,PostSerializer, CommentSerializer, LikeSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import logout
from accounts.company_rating import CompanyRating
from accounts.employee_rating import EmployeeRating
from .serializers import CompanyRatingSerializer, EmployeeRatingSerializer , CompanySerializer ,EmployeeSerializer, CompanyProfileSerializer
from rest_framework.decorators import action
from accounts.company import Company
from rest_framework import viewsets
from accounts.permissions import CanRateCompany, CanRateEmployee
from job.models import JobApplication , Job
from accounts.employee import Employee , Comment ,Post , Like
from job.serializers import JobSerializer , JobbSerializer
from accounts.permissions import *
from django.http import HttpResponse
from rest_framework import serializers



# Create your views here.


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]  # Adjust permissions as needed

    
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
   permission_classes = [AllowAny]
    
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
            'message' : 'The user has been created successfully',
            'user': {
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'employee': {
             "full_name": employee.full_name,
             "nationality": employee.nationality ,
             "phone": employee.phone ,
             "date_of_birth": employee.date_of_birth,
             "gender": employee.gender,
             "job_level": employee.job_level ,
             "edu_level": employee.edu_level,
             "job_status": employee.job_status ,
             "work_city": employee.work_city,
             "job_type": employee.job_type,
             "experience_year":employee.experience_year,
             "salary_range" :employee.salary_range,
             "job_role" : employee.job_role,
             "address": employee.address,
            }
        }

        return Response(data = response_data, status=status.HTTP_201_CREATED)
         
## Login For all 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
## LogOut
class Logout(APIView):
    def delete(self, request):
        try:
            # Check if user is authenticated
            if not request.user.is_authenticated:
                response_data = {
                    'status': 'Error',
                    'message': 'User is not authenticated',
                }
                return Response(data=response_data, status=status.HTTP_401_UNAUTHORIZED)

            # Delete user's authentication token (if applicable)
            # Replace 'auth_token' with the actual field name if using a token library
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()

            # Logout the user
            logout(request)

            response_data = {
                'status': 'Success',
                'message': 'User logged out successfully',
            }
            return Response(data=response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors during logout
            response_data = {
                'status': 'Error',
                'message': f"Logout failed: {str(e)}",
            }
            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        
class CompanyRatingViewSet(viewsets.ModelViewSet):
    queryset = CompanyRating.objects.all()
    serializer_class = CompanyRatingSerializer
    permission_classes = [IsAuthenticated , CanRateCompany]
    
    def list(self, request):
        company_id = request.query_params.get('company_id')
        
        if company_id:
            ratings = self.get_queryset().filter(company_id=company_id)
        else:
            response_data = {
                'status': 'error',
                'message' : 'Comapny ID most be in the query params'
            } 
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        
        ratings = self.get_queryset().filter(company_id=company_id)        
        serializer = self.get_serializer(ratings, many=True)
        response_data = {
                'status': 'success',
                'data' : serializer.data
            }        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        try:
            user = request.user.employee
            company_id = request.data.get('company')
            rating_data = request.data.get('rating')
            comment_data = request.data.get('comment')

            if rating_data is None or comment_data is None:
                return Response({
                    'status': 'error',
                    'message': 'Rating and comment are required fields'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the rating is between 1 and 5
            if not (1 <= rating_data <= 5):
                return Response({
                    'status': 'error',
                    'message': 'Rating must be between 1 and 5'
                }, status=status.HTTP_400_BAD_REQUEST)
            # Check if the employee has already rated this company
            try:
                company_rating = CompanyRating.objects.get(employee=user, company_id=company_id)
                company_rating.rating = rating_data
                company_rating.comment = comment_data
                company_rating.save()

                response_data = {
                    'status': 'success',
                    'message': 'Your review has been updated'
                }

            except CompanyRating.DoesNotExist:
                CompanyRating.objects.create(
                    employee=user, rating=rating_data, comment=comment_data, company_id=company_id
                )

                response_data = {
                    'status': 'success',
                    'message': 'Your review has been submitted'
                }

            return Response(response_data, status=status.HTTP_200_OK)

        except JobApplication.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'An error occurred while checking your application status. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
from django.shortcuts import get_object_or_404


class EmployeeRatingViewSet(viewsets.ModelViewSet):
    queryset = EmployeeRating.objects.all()
    serializer_class = EmployeeRatingSerializer
    permission_classes = [IsAuthenticated , CanRateEmployee]

    def create(self, request, *args, **kwargs):
        user = request.user
        company = get_object_or_404(Company, user=user)

        # Get rating and comment data
        rating_data = request.data.get('rating')
        comment_data = request.data.get('comment')
        employee_id = request.data.get('employee')

        # Check for required fields (rating and comment)
        if rating_data is None or comment_data is None:
                return Response({
                    'status': 'error',
                    'message': 'Rating and comment are required fields'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the rating is between 1 and 5
        if not (1 <= rating_data <= 5):
            return Response({
                'status': 'error',
                'message': 'Rating must be between 1 and 5'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the employee exists
        employee = get_object_or_404(Employee, id=employee_id)
        try:
            employee_rating = EmployeeRating.objects.get(employee=employee, company=company)
            employee_rating.rating = rating_data
            employee_rating.comment = comment_data
            employee_rating.save()

            response_data = {
                'status': 'success',
                'message': 'Your review has been updated'
            }

        except EmployeeRating.DoesNotExist:
        # Create the rating object
            EmployeeRating.objects.create(
            company=company,
            rating=rating_data,
            comment=comment_data,
            employee=employee
        )

        response_data = {
            'status': 'Success',
            'message': 'Your review has been submitted'
        }
        return Response(response_data, status=status.HTTP_200_OK)


    def list(self, request):
        employee_id = request.query_params.get('employee_id')

        if employee_id:
            ratings = self.get_queryset().filter(employee_id=employee_id)
        else:
            response_data = {
                'status': 'error',
                'message': 'Employee ID must be in the query params'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(ratings, many=True)
        response_data = {
            'status': 'success',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
      
"...............Company Profile............."    
    
class CompanyProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path=r'(?P<company_id>\d+)')
    def retrieve_profile(self, request, company_id=None):
        company = get_object_or_404(Company, pk=company_id)
        company_serializer = CompanyProfileSerializer(company , context={'request': request})

        jobs = Job.objects.filter(company=company)
        jobs_serializer = JobbSerializer(jobs, many=True)

        response_data = {
            'status': 'Success',
            'company': company_serializer.data,
            'jobs': jobs_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path=r'(?P<company_id>\d+)/profile')
    def create_or_update_profile(self, request, company_id=None):
        company = get_object_or_404(Company, pk=company_id)
        user = request.user

        # Check if the user is authorized to update the profile
        if company.user != user:
            return Response({
                'status': 'error',
                'message': 'You are not authorized to update this company profile.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Update company profile
        company_serializer = CompanyProfileSerializer(company, data=request.data, partial=True , context={'request': request})
        if company_serializer.is_valid():
            company_serializer.save()
        else:
            return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'status': 'Success',
            'message': 'Company profile updated successfully.',
            'company': company_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)   
    
"...............Employee Profile..........."    
class EmployeeProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path=r'(?P<employee_id>\d+)')
    def retrieve_profile(self, request, employee_id=None):
        employee = get_object_or_404(Employee, pk=employee_id)
        employee_serializer = EmployeeSerializer(employee , context={'request': request})
        
        response_data = {
            'status': 'Success',
            'employee': employee_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path=r'(?P<employee_id>\d+)/update')
    def update_profile(self, request, employee_id=None):
        employee = get_object_or_404(Employee, pk=employee_id)
        user = request.user

        if employee.user != user:
            return Response({
                'status': 'error',
                'message': 'You are not authorized to update this profile.'
            }, status=status.HTTP_403_FORBIDDEN)

        employee_serializer = EmployeeSerializer(employee, data=request.data, partial=True , context={'request': request})
        if employee_serializer.is_valid():
            employee_serializer.save()
            response_data = {
                'status': 'Success',
                'message': 'Profile updated successfully.',
                'employee': employee_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
".................Dashboard................."
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]     
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
    
def home(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome Home</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            .container {
                text-align: center;
                background: white;
                padding: 2em;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to WorkHub</h1>
            <p>Your journey towards a better work experience starts here.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "OTP code has been sent to your email."}, status=status.HTTP_200_OK)
    
class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform the OTP verification and any additional actions here
        return Response({"detail": "OTP verified successfully."}, status=status.HTTP_200_OK)   
    
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployee])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=self.request.user.employee, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsEmployee])
    def like(self, request, pk=None):
        post = self.get_object()
        employee = request.user.employee
        like = Like.objects.filter(post=post, employee=employee).exists()
        liked = Like.objects.filter(post=post, employee=employee)

        if like :
            liked.delete()
            return Response({"status": "Success", "message": "Post unliked"}, status=status.HTTP_201_CREATED)
        
        Like.objects.create(post=post, employee=employee)
        return Response({"status": "Success", "message": "Post liked"}, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsEmployee]    