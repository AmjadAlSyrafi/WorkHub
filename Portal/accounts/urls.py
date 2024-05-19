from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (LoginView , CreateUserView , RegisterEmployeeView , RegisterCompanyView)


urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("register/company/", RegisterCompanyView.as_view(), name="register_company"),
    path("register/employee/", RegisterEmployeeView.as_view(), name="register_employee"), 
    ##path("logout/", MyTokenObtainPairView.as_view(), name="LogOut"),
   
]   