from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (MyTokenObtainPairView , RegisterCompanyView , RegisterEmployeeView)


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/Company/", RegisterCompanyView.as_view(), name="register_company"),
    path("register/employee/", RegisterEmployeeView_view(), name="register_employee"), 
    path("logout/", MyTokenObtainPairView.as_view(), name="LogOut"),
   
]