from django.urls import path
from .views import StudentSignUpView, EmployeeSignUpView, Login, Logout

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', StudentSignUpView.as_view(), name = 'student-signup'),
    path('employee-signup/', EmployeeSignUpView.as_view(), name = 'employee-signup'),
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'logout'),

    
]