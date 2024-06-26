from rest_framework import serializers
from .models import Job
from .models import Favorite
from accounts.company import Company
from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.employee import Employee
from accounts.serializers import EmployeeSerializer
from .models import JobApplication 


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'location']



class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id',
            'job_name', 'job_role', 'job_level', 'experience','languages',
            'job_type', 'salary', 'gender', 'education','city', 'about','case','age_min',
            'age_max','job_description' ,'job_requirements' ,  'company'
        ]
        read_only_fields = ['posted_at'] 
        

class JobUpdateSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Job
        fields = [
            'job_name', 'job_role', 'job_level', 'experience','languages',
            'job_type', 'salary', 'gender', 'education','city', 'about','case','age_min',
            'age_max','job_description' ,'job_requirements' ,  'company'
        ]
          
        

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = [
        'user',
        'job', 
        'is_favorite', 
        'created_at',
        ]

class ListFavoriteSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = [
        'job', 
        'is_favorite', 
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'employee','company', 'job', 'cv', 'motivation_letter', 'status', 'date_submitted']
        read_only_fields = ['employee','company', 'job', 'status', 'date_submitted']


class EmployeeJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['cv', 'motivation_letter']

class CompanyJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']