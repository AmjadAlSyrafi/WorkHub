from rest_framework.permissions import BasePermission
from job.models import Job
from accounts.company import Company
from job.models import JobApplication
class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Company'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Employee'
    
class IsJobCreator(BasePermission):
    # message = 'Permission denied'

    def has_permission(self, request, view):
        job_id = view.kwargs.get("job_id")
        user=request.user
        company = Company.objects.get(user=user)
        
        if job_id:
            if Job.objects.filter(id=job_id, company=company).exists():
                return True
            else:
                return False
        return False    
    
class CanRateCompany(BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is POST
        if request.method != 'POST':
            return True
        
        try:
            user = request.user.employee  
            company_id = request.data.get('company')

            if not company_id:
                return False

            # Check if the user has an approved job application for the company
            return JobApplication.objects.filter(
                employee=user, company_id=company_id, status='accepted'
            ).exists()
        except AttributeError:
            return False
        
class CanRateEmployee(BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is POST
        if request.method != 'POST':
            return True
        
        try:
            user = request.user.id

            employee_id = request.data.get('employee')

            if not user:
                return False

            # Check if the user has an approved job application for the company
            return JobApplication.objects.filter(
                employee_id=employee_id, company=user, status='accepted'
            ).exists()
        except AttributeError:
            return False  


  
