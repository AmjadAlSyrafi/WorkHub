from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    edu_level = models.CharField(max_length=100)
    job_status = models.CharField(max_length=50)
    job_level = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    work_city = models.CharField(max_length=50)
    experience_year = models.IntegerField(validators=[MinValueValidator(0)])
    salary_range = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
