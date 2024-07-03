from django.db import models
from django.core.validators import MinValueValidator ,MaxValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.conf import settings
User = get_user_model()

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    employee_count = models.IntegerField(validators=[MinValueValidator(1)])
    field_work = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    average_rating = models.FloatField(default=0.0) 
    profile_picture = models.ImageField(upload_to='company_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
       
    def update_average_rating(self):
        self.average_rating = self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0.0
        self.save()

    def __str__(self):
        return self.user.username
