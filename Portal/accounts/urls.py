from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import (MyTokenObtainPairView , Logout , RegisterEmployeeView , RegisterCompanyView)


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/company/", RegisterCompanyView.as_view(), name="register_company"),
    path("register/employee/", RegisterEmployeeView.as_view(), name="register_employee"), 
    path("logout/", Logout.as_view(), name="LogOut"),
   
]   