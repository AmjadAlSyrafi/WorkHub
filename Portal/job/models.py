from django.db import models
from accounts.company import Company
from accounts.employee import Employee
from django.utils import timezone
from accounts.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

class Job(models.Model):
    JOB_LEVEL_CHOICES = [
        ('Entry', 'Entry'),
        ('Jenior', 'Jenior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior')
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('Any', 'Any')
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    job_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100)
    job_level = models.CharField(max_length=50, choices=JOB_LEVEL_CHOICES)
    experience = models.PositiveIntegerField()
    job_type = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    education = models.CharField(max_length=100)
    about = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    job_description = models.TextField()
    job_requirements = models.TextField()
    languages = models.CharField(max_length=50)
    age_min = models.PositiveIntegerField(validators=[MinValueValidator(18)], default=18)  
    age_max = models.PositiveIntegerField(validators=[MaxValueValidator(65)], default=65)
    city = models.CharField(max_length=50)

    
    
    
    def __str__(self):
        return self.job_name



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.job.job_name


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job = models.ForeignKey(Job ,on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/', validators=[FileExtensionValidator(['pdf'])])
    motivation_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_submitted = models.DateTimeField(auto_now_add=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    meeting_link = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.name} - {self.get_status_display()}"