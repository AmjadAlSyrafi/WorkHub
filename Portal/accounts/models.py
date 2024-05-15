from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYEE = 'Employee', 'employee'
        COMPANY = 'Company', 'company'

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=Role.choices, max_length=10, default=Role.EMPLOYEE)
    reset_password_token = models.CharField(max_length=50, default="", blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Unique related_name for groups
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Unique related_name for user_permissions
        related_query_name='user'
    )

    USERNAME_FIELD = 'email'
    
    object = UserManager()

    def __str__(self):
        return self.username