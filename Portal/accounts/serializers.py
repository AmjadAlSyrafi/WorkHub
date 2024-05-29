from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from accounts.company import Company
from accounts.employee import Employee
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()
##------------------------------------------------------------------------------------------------##

## I created Serializers for each type user... mafi lil ejari liliii mafi lil 
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            'password',
            'confirm_password'
        )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            '__all__'
        )
        
class CreateCompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Company
        fields = ('user','company_name', 'location', 'employee_count', 'field_work', 'phone_number')
        
    def validate(self, attrs):
        employee_count = attrs.get('employee_count')
        if employee_count and employee_count < 1:
            raise serializers.ValidationError("Employee count must be at least 1.")
        
        return attrs
        
class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = (
            '__all__'
        )

##Company
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)  # Maintain for informative purposes

    class Meta:
        model = User
        fields = ('username', 'email','confirm_password','password', 'role')  # Exclude 'role' from fields

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs


class RegisterCompanySerializer(serializers.Serializer):
    user = UserCreateSerializer(required=True)
    company = CreateCompanySerializer(required=True)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        company_data = validated_data.pop('company')    

        # Create user
        user_data.pop("confirm_password")
        user = User.objects.create_user(**user_data)

        # Create company
        company_data['user'] = user  # Assign the created user to the company
        company = Company.objects.create(**company_data)

        return {
            'user': user,
            'company': company
        }
        
##Employee
class CreateEmployeeSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = (
            "user",
            "full_name",
            "nationality",
            "phone",
            "date_of_birth",
            "gender",
            "job_level" ,
            "edu_level",
            "job_status" ,
            "work_city",
            "job_type",
            "experience_year",
            "salary_range",
            "address",
            "job_role"
        )
    def validate(self, attrs):
         experience_year = attrs.get('experience_year')  
         if experience_year < 1 :
            raise serializers.ValidationError("Employee Experience_year must be at least 1.")
         salary_range = attrs.get('salary_range')  
         if salary_range < 50000 :
            raise serializers.ValidationError("Salary range must be at least 50000.") 

         return attrs

class RegisterEmployeeSerializer(serializers.Serializer):
    user = UserCreateSerializer(required=True)
    employee = CreateEmployeeSerializer(required=True)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        employee_data = validated_data.pop('employee')

        # Create user
        user_data.pop('confirm_password')
        user = User.objects.create_user(**user_data)

        # Create employee
        employee_data['user'] = user  # Assign the created user to the employee
        employee = Employee.objects.create(**employee_data)

        return {
            'user': user,
            'employee': employee
        }        
    
## login with make acsses and refresh token for all
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Ensure email and password are provided
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate the user using email and password
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Incorrect email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate tokens using the default mechanism
        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['email'] = user.email
        token['username'] = user.username
        return token

