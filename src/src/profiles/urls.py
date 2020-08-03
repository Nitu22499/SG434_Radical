from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('student-update/<int:stud>', StudentUpdateView.as_view(), name = 'student-update'),
    path('student-signup/', StudentSignUpView.as_view(), name = 'student-signup'),
    path('', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('student-list/', StudentList.as_view(), name = 'student-list'),
    path('student-list/<int:stud>', StudentInfo.as_view(), name = 'student-info'),
    path('school-register/', SchoolRegisterView.as_view(), name = 'school-register'),
    path('school-list/', SchoolList.as_view(), name = 'school-list'),
]