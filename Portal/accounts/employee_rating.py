from django.db import models
from django.core.validators import MinValueValidator ,MaxValueValidator
from accounts.company import Company
from accounts.employee import Employee

class EmployeeRating(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ratings')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.employee.update_average_rating()