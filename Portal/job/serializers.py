from rest_framework import serializers
from .models import Job
from accounts.company import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'location']


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Job
        fields = [
            'id', 'job_name', 'job_role', 'job_level', 'experience', 
            'job_type', 'salary', 'gender', 'education', 'about','posted_at', 'case', 'company'
        ]
        read_only_fields = ['posted_at'] 
        

        
        
           
        