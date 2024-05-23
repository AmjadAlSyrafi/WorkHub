from rest_framework import generics, permissions , status
from .models import Job
from .serializers import JobSerializer , JobUpdateSerializer
from accounts.permissions import *
from accounts.company import Company
from rest_framework.response import Response
from rest_framework.views import APIView




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
                         "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    
