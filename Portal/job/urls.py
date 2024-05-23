from django.shortcuts import render
from .views import JobCreateView , CompanyJobListView , JobUpdateView
from django.urls import path


urlpatterns = [
    #*******    COMPANY JOB URLS   **********
    path('create/', JobCreateView.as_view(), name='create-job'),
    path('company-jobs/', CompanyJobListView.as_view(), name='job-list'),
    path('company-jobs/<int:job_id>/', JobUpdateView.as_view(), name='company-job-update'),

    # ******        ee                ***********
    
    
    
    
]