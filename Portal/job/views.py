from rest_framework import generics, permissions , status
from .models import Job , Favorite, JobApplication
from .serializers import EmployeeJobApplicationSerializer, JobApplicationSerializer, JobSerializer , JobUpdateSerializer, ListFavoriteSerializer
from accounts.permissions import *
from accounts.company import Company
from accounts.employee import Employee
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

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
    

class JobSearchView(APIView):
    def get(self, request, format=None):
        # Get the search keyword from the request
        keyword = request.GET.get('keyword')

        # Build the Django query using icontains for fuzzy matching
        query = Job.objects.filter(case=True)
        if keyword:
            query = query.filter(Q(job_name__icontains=keyword))

        # Retrieve and serialize the results (handle no results)
        jobs = query.all()
        if not jobs.exists():
            return Response({'message': 'No jobs found matching your search criteria.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data , status=status.HTTP_200_OK)
    
class CompanyJobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()  
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsCompany] 

    @action(detail=False, methods=['get'], url_path='my-applications')
    def list_my_applications(self, request):

        queryset = self.get_queryset()
        page = PageNumberPagination()
        paginated_queryset = page.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        instance = self.get_object()
        status_data = request.data.get('status')

        if status_data not in ['accepted', 'rejected']:
            return Response({'error': 'Invalid status. Only \'accepted\' or \'rejected\' allowed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure the application belongs to the company the admin manages
        if instance.job.company != self.request.user.company:
            return Response({'error': 'You cannot update applications for another company.'},
                            status=status.HTTP_403_FORBIDDEN)

        instance.status = status_data
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated , IsEmployee] 

    @action(detail=False, methods=['post'], url_path=r'(?P<job_id>\d+)/apply')
    def create_application(self, request, job_id=None):
        motivation_letter = request.data.get('motivation_letter')
        cv = request.FILES.get('cv')
        user = request.user

        job = get_object_or_404(Job, pk=job_id)
        employee = get_object_or_404(Employee, user=user)
        company = job.company

        job_application = JobApplication.objects.create(
            job=job,
            employee=employee,
            company=company,
            motivation_letter=motivation_letter,
            cv=cv
        )

        serializer = self.get_serializer(job_application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='update-application')
    def update_application(self, request, pk=None):
        instance = self.get_object()

        if instance.employee.user != request.user:
            return Response({"error": "You do not have permission to edit this job application."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = EmployeeJobApplicationSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Update specific fields
        instance.cv = request.data.get('cv', instance.cv)  # Update cv if provided in request
        instance.motivation_letter = request.data.get('motivation_letter', instance.motivation_letter)  # Update motivation_letter if provided in request

        instance.save()

        response_data = {
            "status": "Your Information Has Been Updated Succesfully",
            "Your Info": EmployeeJobApplicationSerializer(instance).data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='my-applications')
    def list_my_applications(self, request):

        queryset = self.get_queryset()
        page = PageNumberPagination()
        paginated_queryset = page.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)