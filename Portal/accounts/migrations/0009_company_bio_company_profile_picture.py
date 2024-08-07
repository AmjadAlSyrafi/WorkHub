# Generated by Django 5.0.6 on 2024-07-01 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_company_average_rating_employee_average_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='company_pics/'),
        ),
    ]
