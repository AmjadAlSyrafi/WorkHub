from rest_framework.permissions import BasePermission

class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Company'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Employee'
