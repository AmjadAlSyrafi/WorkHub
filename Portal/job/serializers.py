from rest_framework import serializers
from .models import Job
from .models import Favorite
from accounts.company import Company
from accounts.models import User
from accounts.serializers import UserSerializer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'location']



class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = Job
        fields = [
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
