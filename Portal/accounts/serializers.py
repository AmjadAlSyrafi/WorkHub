from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from accounts.company import Company
from accounts.employee import Employee
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

## Rigester For each type user ma niga 

##ُEmployee
class RegisterEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

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

    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


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
    
## login with make acsses and refresh token for all
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")

        # Check if either email or username is provided ..HOA HOA HOA 
        if not (email or username):
            raise serializers.ValidationError("You must provide either email or username.")

        # Authenticate the user based on provided email or username ... ma dkt ana  noo oo oom
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                user = User.objects.get(email=email)
                user = authenticate(email=email, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError("This email is not registered.")

        # Check if authentication was successful 
        if user:
            data = super().validate(attrs)
            data["username"] = user.username
            return data 
        else:
            raise serializers.ValidationError("Incorrect email/username or password.")

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

