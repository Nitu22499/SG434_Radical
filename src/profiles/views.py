from django.views.generic import CreateView
from .models import User
from .forms import StudentSignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from datetime import date

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'profiles/student-signup.html'
    success_url = reverse_lazy('profiles:student-signup')

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.stud_school = self.request.user.school
        self.object.save()
        return super().form_valid(form)

class Login(LoginView):
    template_name = 'profiles/login.html'

class Logout(LogoutView):
    pass
