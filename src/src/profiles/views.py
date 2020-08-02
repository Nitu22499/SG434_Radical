from django.views.generic import CreateView,ListView
from .models import User, Student
from .forms import StudentSignUpForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

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
        messages.success(self.request, 'Student added successfully')
          
        return super().form_valid(form)

class Login(LoginView):
    template_name = 'profiles/login.html'

class Logout(LogoutView):
    pass

class StudentList(ListView):
    model = Student
    template_name = 'profiles/student-list.html'
    stud_class=""
    stud_section=""

    def get_context_data(self, **kwargs):
        section_choices=['A','B','C', 'D', 'E','F']
        class_choices=['1','2','3','4','5','6','7', '8', '9', '10', '11', '12', 'LKG', 'UKG']
        stream_choices=['Commerce','Electrical Technology','Humanities','Information Technology','PCM','PCB','Tourism','NA']
        kwargs['stream_list'] = stream_choices
        kwargs['section_list'] = section_choices
        kwargs['class_list'] = class_choices
        self.stud_class = self.request.GET.get('input_class')
        # print(self.stud_class)
        self.stud_section = self.request.GET.get('input_section')
        # print(self.stud_section)
        self.stud_stream = self.request.GET.get('input_stream')
        # print(self.stud_stream)
        if(self.stud_stream=="Select Stream" or self.stud_stream==None):
            self.stud_stream="NA"
            # print(self.stud_stream)
        if(self.stud_class=="Select Class"):
            self.stud_class=None
        if(self.stud_section=="Select Section"):
            self.stud_section=None
        student=Student.objects.filter(stud_class=self.stud_class,stud_section=self.stud_section,stud_stream=self.stud_stream)
        print(student)
        # print(student.stud_rollno)
        # print(student)
        kwargs['currentclass']=self.stud_class
        kwargs['currentsection']=self.stud_section
        kwargs['currentstream']=self.stud_stream
        kwargs['student']=student
        return super().get_context_data(**kwargs)

class StudentInfo(ListView):
    model = Student
    template_name = 'profiles/student-info.html'
    context_object_name="stud"

    # def get_queryset(self):
    #     print(self.kwargs['stud'])
    #     stud = Student.objects.get(user__first_name=self.kwargs['stud'])
    #     print(stud.stud_rollno)
    #     return stud

    
    def get_context_data(self, **kwargs):
        stud = Student.objects.get(id=self.kwargs['stud'])
        print(stud.stud_rollno)
        kwargs['stud']=stud
        print(kwargs['stud'])
        return super().get_context_data(**kwargs)



    