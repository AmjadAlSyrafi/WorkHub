from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobApplicationViewSet,
    JobCreateView, 
    CompanyJobListView, 
    JobUpdateView, 
    JobSearchView, 
    FavoriteJobListView, 
    favorite_status, 
    FilteredJobListView, 
    AllJobListView, 
    CompanyJobApplicationViewSet,
    JobForAdmin,
    JobAppForAdmin
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'company/job-applications', CompanyJobApplicationViewSet, basename='company-job-application')
router.register(r'employee/job-applications', JobApplicationViewSet, basename='employee-job-application')
router.register(r'admin/job', JobForAdmin, basename='admin-job')
router.register(r'admin/job-app', JobAppForAdmin, basename='admin-job-app')



urlpatterns = [
    # Company job URLs
    path('create/', JobCreateView.as_view(), name='create-job'),
    path('company-jobs/', CompanyJobListView.as_view(), name='job-list'),
    path('company-jobs/<int:job_id>/', JobUpdateView.as_view(), name='company-job-update'),

    # Favorite job URLs
    path('favorites/<int:job_id>/', favorite_status, name='favorite_status'),
    path('favorite-jobs/', FavoriteJobListView.as_view(), name='favorite-jobs'),
    path('custom/', FilteredJobListView.as_view(), name='custom-jobs'),
    path('search/', JobSearchView.as_view(), name='search-jobs'),
    path('', AllJobListView.as_view(), name='all-jobs'),

    # Include router URLs
    path('', include(router.urls)),
    
]