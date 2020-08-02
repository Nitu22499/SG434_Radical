from django.urls import path
from .views import StudentSignUpView, Login, Logout

app_name = 'profiles'

urlpatterns = [
    path('student-signup/', StudentSignUpView.as_view(), name = 'student-signup'),
    path('', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'logout'),

    
]