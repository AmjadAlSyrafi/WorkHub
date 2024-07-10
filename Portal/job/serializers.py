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


class JobbSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    posted_at = serializers.ReadOnlyField()
    class Meta:
        model = Job
        fields = [
            'id', 'job_name', 'job_role', 'job_level', 'experience', 'languages',
            'job_type', 'salary', 'gender', 'education', 'city', 'about', 'active', 
            'age_min', 'age_max', 'job_description', 'job_requirements', 'company', 
            'posted_at'
        ]
        
class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    posted_at = serializers.ReadOnlyField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'job_name', 'job_role', 'job_level', 'experience', 'languages',
            'job_type', 'salary', 'gender', 'education', 'city', 'about', 'active', 
            'age_min', 'age_max', 'job_description', 'job_requirements', 'company', 
            'posted_at', 'is_favorite'
        ]

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, job=obj).exists()
        return False
        

class JobUpdateSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    posted_at = serializers.ReadOnlyField()

    class Meta:
        model = Job
        fields = [
            'job_name', 'job_role', 'job_level', 'experience','languages',
            'job_type', 'salary', 'gender', 'education','city', 'about','active','age_min',
            'age_max','job_description' ,'job_requirements' ,  'company','posted_at'
        ]
          
        

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = [
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
    employee = EmployeeSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = JobApplication
        fields = ['id', 'employee','job', 'cv', 'motivation_letter', 'status', 'date_submitted']
        read_only_fields = ['employee','company', 'job', 'status', 'date_submitted']


class EmployeeJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['cv', 'motivation_letter']

class CompanyJobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']