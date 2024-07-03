from django.urls import path ,include
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import (MyTokenObtainPairView , Logout , RegisterEmployeeView , 
                    RegisterCompanyView ,CompanyRatingViewSet, EmployeeRatingViewSet , EmployeeProfileViewSet ,
                    CompanyViewSet , EmployeeViewSet,CompanyProfileViewSet)

from rest_framework.routers import DefaultRouter ,SimpleRouter
from django.conf import settings
from django.conf.urls.static import static


router_default = DefaultRouter()
router_default.register(r'company-ratings', CompanyRatingViewSet)
router_default.register(r'employee-ratings', EmployeeRatingViewSet)
router_default.register(r'company-profile', CompanyProfileViewSet, basename='company-profile')
router_default.register(r'employee-profile', EmployeeProfileViewSet, basename='employee-profile')


router_simple = SimpleRouter()
router_simple.register(r'companies', CompanyViewSet)
router_simple.register(r'employees', EmployeeViewSet)



urlpatterns = [
    path('', include(router_default.urls)),
    path('', include(router_simple.urls)),  # Include both router URL patterns
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/company/", RegisterCompanyView.as_view(), name="register_company"),
    path("register/employee/", RegisterEmployeeView.as_view(), name="register_employee"),
    path("logout/", Logout.as_view(), name="LogOut"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)