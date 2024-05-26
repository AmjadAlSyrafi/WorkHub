from django.shortcuts import render
from .views import JobCreateView , CompanyJobListView , JobUpdateView , FavoriteJobListView ,favorite_status
from django.urls import path


urlpatterns = [
    #*******    COMPANY JOB URLS   **********
    path('create/', JobCreateView.as_view(), name='create-job'),
    path('company-jobs/', CompanyJobListView.as_view(), name='job-list'),
    path('company-jobs/<int:job_id>/', JobUpdateView.as_view(), name='company-job-update'),
    path('favorites/<int:job_id>/', favorite_status, name='favorite_status'),
    path('favorite-jobs/<int:user_id>/', FavoriteJobListView.as_view(), name='favorite-jobs'),
    # ******        ee                ***********
    
    
    
    
]