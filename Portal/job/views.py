from rest_framework import generics, permissions , status
from .models import Job
from .serializers import JobSerializer
from accounts.permissions import IsCompany
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
