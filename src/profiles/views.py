from django.views.generic import CreateView
from .models import User
from .forms import StudentSignUpForm, EmployeeSignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'profiles/student-signup.html'
    success_url = reverse_lazy('profiles:student-signup')


class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'profiles/employee-signup.html'
    success_url = reverse_lazy('profiles:employee-signup')


class Login(LoginView):
    template_name = 'profiles/login.html'

class Logout(LogoutView):
    pass
