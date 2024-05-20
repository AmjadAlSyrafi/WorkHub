from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.manager import UserManager
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
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
    REQUIRED_FIELDS = []
    object = UserManager()

    def __str__(self):
        return self.username