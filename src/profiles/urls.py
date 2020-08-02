from django.urls import path
from .views import StudentSignUpView, Login, Logout, StudentList, StudentInfo

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', StudentSignUpView.as_view(), name = 'student-signup'),
    path('', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('student-list/', StudentList.as_view(), name = 'student-list'),
    path('student-list/<int:stud>', StudentInfo.as_view(), name = 'student-info'),

    
]