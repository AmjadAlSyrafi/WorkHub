from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from accounts.company import Company
from accounts.employee import Employee , Comment ,Post , Like
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.company_rating import CompanyRating
from accounts.employee_rating import EmployeeRating
from django.core.mail import send_mail
from django.conf import settings
import random


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
            'id',
            "username",
            "email",
            "role",
            'password',
            'confirm_password'
        )

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        profile_picture = serializers.ImageField(max_length=None, use_url=True)        
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
    profile_picture = serializers.ImageField(max_length=None, use_url=True)        
    class Meta:
        model = Company
        fields = (
            '__all__'
        )

class CompanyProfileSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    profile_picture = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Company
        fields = ['bio', 'average_rating','profile_picture'] 
        
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

        # Prepare the response data
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,
            'email': user.email
        }

        # If the user role is Employee, include the employee_id
        if user.role == 'Employee': 
            try:
                employee = Employee.objects.get(user=user)
                response_data['employee_id'] = employee.id
            except Employee.DoesNotExist:
                raise serializers.ValidationError("Employee data not found for the user.")

        return response_data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['email'] = user.email
        token['username'] = user.username
        return token


class CompanyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRating
        fields = ['company','employee','rating', 'comment']
        

class EmployeeRatingSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    class Meta:
        model = EmployeeRating
        fields = ['employee','company', 'rating', 'comment']
        
        
class CustomPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address")
        return value

    def save(self):
        user = self.user
        otp = random.randint(100000, 999999)
        user.otp_code = otp
        user.save()
        
        subject = 'Your WorkHub OTP Code for Password Reset'
        message = f'Your OTP code is {otp}. Please use this code to reset your password. WorkHub Team!.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list)        
        
        
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email address")

        if user.otp_code != data['otp_code']:
            raise serializers.ValidationError("Invalid OTP code")

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.otp_code = None  # Clear the OTP code after use
        user.save()
        return user        
    
    
class CommentSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='employee.user.email')

    class Meta:
        model = Comment
        fields = ['id', 'employee', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='employee.user.email')

    class Meta:
        model = Like
        fields = ['id', 'employee', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    employee = serializers.ReadOnlyField(source='employee.user.email')
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'employee', 'content', 'created_at', 'comments', 'likes', 'likes_count']    