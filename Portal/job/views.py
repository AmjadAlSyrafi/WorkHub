from rest_framework import generics, permissions , status
from .models import Job , Favorite
from .serializers import JobSerializer , JobUpdateSerializer, ListFavoriteSerializer
from accounts.permissions import *
from accounts.company import Company
from accounts.employee import Employee
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated , IsCompany]

    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            # Get the authenticated user
            user = request.user
            
            # Retrieve the company associated with the user
            try:
                company = Company.objects.get(user=user)
            except Company.DoesNotExist:
                return Response(
                    {"status": "Error", "message": "Company does not exist for the authenticated user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save the job with the associated company
            job = serializer.save(company=company)
            
            response_data = {
                "status": "Success",
                "message": "Job created successfully.",
                "job": JobSerializer(job).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({"status": "Error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class CompanyJobListView(APIView):
    permission_classes = [permissions.IsAuthenticated , IsCompany]

    def get(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Retrieve the company associated with the user
        try:
            company = Company.objects.get(user=user)
        except Company.DoesNotExist:
            return Response(
                {"status": "Error", "message": "Company does not exist for the authenticated user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter jobs by the company
        jobs = Job.objects.filter(company=company)
        serializer = JobSerializer(jobs, many=True)
        
        response_data = {
            "status": "Success",
            "jobs": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)    
    
class JobUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated , IsCompany , IsJobCreator]

    def patch(self, request, job_id, *args, **kwargs):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"status": "Error", "message": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobUpdateSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Success", "message": "Job updated successfully.",
                             "job": serializer.data}, status=status.HTTP_200_OK)
            
        return Response({"status": "Error", "message": "Invalid data.",
                         "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_status(request, job_id):
    user = request.user
    job = Job.objects.get(id=job_id)

    try:
        favorite = Favorite.objects.get(user=user, job_id=job_id)
        favorite.is_favorite = not favorite.is_favorite  # Toggle favorite status
        favorite.save()
        return Response({'is_favorite': favorite.is_favorite}, status=status.HTTP_200_OK)

    except Favorite.DoesNotExist:
        favorite, created = Favorite.objects.get_or_create(user=user, job=job)
        favorite.is_favorite = True  # Set favorite to True for new entry
        favorite.save()
        return Response({
            'is_favorite': favorite.is_favorite}, status=status.HTTP_200_OK)


class FavoriteJobListView(generics.ListAPIView):
    serializer_class = ListFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Retrieve the authenticated user
        user = self.request.user
        # Get favorite jobs for the user
        return Favorite.objects.filter(user=user, is_favorite=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "Success",
            "jobs":serializer.data
        }
        
        return Response(response_data)  
    
    
class FilteredJobListView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        user = self.request.user 
        
        employee = Employee.objects.get(user = user)
        employee_job_role= employee.job_role
            # Filter by employee's job role by default
        queryset = queryset.filter(job_role=employee_job_role)
        
        if not queryset.exists() :
            queryset = Job.objects.all()
            
        city = self.request.query_params.get('city', None)
        job_role = self.request.query_params.get('job_role', None)
        job_type = self.request.query_params.get('job_type', None)
        job_level = self.request.query_params.get('job_level', None)


        if job_role:
            queryset = Job.objects.all()    
            queryset = queryset.filter(job_role=job_role)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if job_level:
            queryset = queryset.filter(job_level=job_level)
        if city:
            queryset = queryset.filter(city=city)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = self.request.user 
        employee = Employee.objects.get(user = user)
        employee_job_role= employee.job_role
        if not queryset.exists():
            return Response({"status": "Error",
                             "message": "No jobs found matching the criteria"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "Success",
            "job_role":employee_job_role,
            "jobs":serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class AllJobListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()
        return queryset.distinct()  # Remove potential duplicates

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"status": "Error",
                             "message": "No jobs found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            "status": "Success",
            "jobs": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    


