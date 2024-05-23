from django.db import models
from accounts.company import Company
from django.utils import timezone

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
    case = models.BooleanField(default=True)
    
    def __str__(self):
        return self.job_name
