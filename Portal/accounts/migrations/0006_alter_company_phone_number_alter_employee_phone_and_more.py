# Generated by Django 4.2.5 on 2024-05-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_employee_gender_alter_employee_salary_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone_number',
            field=models.IntegerField(max_length=15),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.IntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary_range',
            field=models.IntegerField(max_length=100),
        ),
    ]