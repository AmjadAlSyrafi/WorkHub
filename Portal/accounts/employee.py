from django.db import models
from django.core.validators import MinValueValidator ,MaxValueValidator
from django.contrib.auth import get_user_model
from accounts.company import Company    
from django.db.models import Avg

User = get_user_model()

class Employee(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=50)
    job_status = models.CharField(max_length=50)
    job_level = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    work_city = models.CharField(max_length=50)
    experience_year = models.IntegerField(validators=[MinValueValidator(0)])
    salary_range = models.IntegerField()
    address = models.CharField(max_length=50)
    job_role = models.CharField(max_length=50)
    average_rating = models.FloatField(default=0.0)
    profile_picture = models.ImageField(upload_to='employee_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def update_average_rating(self):
        self.average_rating = self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0.0
        self.save()    

    def __str__(self):
        return self.user.username
    
    
class Post(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.employee.user.email}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.employee.user.email} on {self.post.id}"

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.employee.user.email} on {self.post.id}"        
