from rest_framework.permissions import BasePermission
from job.models import Job
from accounts.company import Company
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
