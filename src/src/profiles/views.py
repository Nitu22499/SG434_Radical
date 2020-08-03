from django.views.generic import CreateView,ListView,FormView,UpdateView,DeleteView
from .models import *
from schoolinfo.models import SchoolProfile
from .forms import *
from schoolinfo.forms import SectionHomeForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from datetime import date,datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.forms.models import model_to_dict
from misc.utilities import academic_year

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
        # stream_choices=['COMMERCE','ELECTRICAL TECHNOLOGY','HUMANITIES','INFORMATION TECHNOLOGY','PCM','PCB','TOURISM','NA']
        stream_choices=[('COMMERCE', 'COMMERCE'), ('ELECTRICAL TECHNOLOGY', 'ELECTRICAL TECHNOLOGY'), ('HUMANITIES', 'HUMANITIES'), ('INFORMATION TECHNOLOGY', 'INFORMATION TECHNOLOGY'), ('PCM', 'PCM'), ('PCB', 'PCB'), ('TOURISM', 'TOURISM')]
        school = School.objects.all()
        # print(school)
        kwargs['school_list'] = school
        kwargs['stream_list'] = stream_choices
        # print(kwargs['stream_list'])
        kwargs['section_list'] = section_choices
        kwargs['class_list'] = class_choices
        self.stud_school = self.request.GET.get('input_school')
        # print(self.stud_school)
        self.stud_class = self.request.GET.get('input_class')
        print(self.stud_class)
        self.stud_section = self.request.GET.get('input_section')
        print(self.stud_section)
        self.stud_stream = self.request.GET.get('input_stream')
        print(self.stud_stream)
        
        if(self.stud_stream is None):
            self.stud_stream="NA"
            print(self.stud_stream)
        # print(self.request.user)
        if(self.request.user.is_school_admin):
            student=Student.objects.filter(stud_school=self.request.user.school,stud_class=self.stud_class,stud_section=self.stud_section,stud_stream=self.stud_stream)
            print(student)
            if student:
                kwargs['currentclass']=self.stud_class
                kwargs['currentsection']=self.stud_section
                kwargs['currentstream']=self.stud_stream
                kwargs['student']=student
                return super().get_context_data(**kwargs)
            else:
                kwargs['currentclass']=None
                kwargs['currentsection']=None
                kwargs['currentstream']=None
                # kwargs['student']=student
                return super().get_context_data(**kwargs)
            
        else:
            obj=Student.objects.filter(stud_school=self.stud_school,stud_class=self.stud_class,stud_section=self.stud_section,stud_stream=self.stud_stream)
            #print(obj)
            if obj:
                kwargs['currentclass']=self.stud_class
                kwargs['currentsection']=self.stud_section
                kwargs['currentstream']=self.stud_stream
                kwargs['currentschool']=self.stud_school
                kwargs['student']=obj
                return super().get_context_data(**kwargs)
            else:
                kwargs['currentclass']=None
                kwargs['currentsection']=None
                kwargs['currentstream']=None
            
                return super().get_context_data(**kwargs)
        
        # print(student.stud_rollno)
        # print(student)
        

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
        # print(stud.stud_rollno)
        kwargs['stud']=stud
        # print(kwargs['stud'])
        return super().get_context_data(**kwargs)

class StudentUpdateView(FormView):
    form_class = StudentUpdateForm
    template_name = 'profiles/student-update-info.html'
    success_url = reverse_lazy('profiles:student-list')
    
    def get_object(self):
        """Check if data already exists"""
        try:
            self.object = Student.objects.get(id = self.kwargs['stud'])
            return self.object
        except:
            return None

    def get_initial(self):
        """Pre-fill the form if data exists"""
        obj = self.get_object()
        if obj is not None:
            initial_data = model_to_dict(obj)
            initial_data.update(model_to_dict(obj.user))
            return initial_data
        else:
            return super().get_initial()

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        User.objects.filter(id=self.object.user.id).update(
            first_name = form.cleaned_data['first_name'],
            middle_name = form.cleaned_data['middle_name'],
            last_name = form.cleaned_data['last_name'],
            gender = form.cleaned_data['gender'],
            date_of_birth = form.cleaned_data['date_of_birth']
        )
        if not form.cleaned_data['stud_stream']:
            form.cleaned_data['stud_stream'] = 'NA'

        Student.objects.filter(id=self.kwargs['stud']).update(
            stud_mother_name = form.cleaned_data['stud_mother_name'],
            stud_class = form.cleaned_data['stud_class'], 
            stud_section = form.cleaned_data['stud_section'],
            stud_rollno = form.cleaned_data['stud_rollno'],
            
            stud_stream = form.cleaned_data['stud_stream'],
            stud_religion = form.cleaned_data['stud_religion'],
            stud_socialCategory = form.cleaned_data['stud_socialCategory'],
            stud_caste = form.cleaned_data['stud_caste'],
            stud_disability = form.cleaned_data['stud_disability'],
            stud_admissionDate = form.cleaned_data['stud_admissionDate'],
            stud_parentContact = form.cleaned_data['stud_parentContact'],
            stud_parentSecContact = form.cleaned_data['stud_parentSecContact'],
            stud_address = form.cleaned_data['stud_address'],
        )

        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form) 


class StudentDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('profiles:student-list')


class SchoolRegisterView(CreateView):
    model = User
    form_class = SchoolSignUpForm
    template_name = 'profiles/school-register.html'
    success_url = reverse_lazy('profiles:school-list')

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.save()
        school_profile_obj = SchoolProfile(academic_year = academic_year(),
            sp_school = self.object,
            sp_school_name = self.object.school_name,
            sp_cd=self.object.school_block.block_name
        )
        school_profile_obj.save()
        messages.success(self.request, 'School Registered successfully')
          
        return super().form_valid(form)


class SchoolList(FormView):
    model = SchoolProfile
    template_name = 'profiles/school-list.html'
    form_class = SchoolListForm
    academic_year_field = ''
    districts_field = None
    blocks_field = None
    categories_field = None
    management_field = None

    def get(self, request, *args, **kwargs):
        self.academic_year_field = self.request.GET.get('academic_year_field')
        # print(self.academic_year_field)
        if self.request.GET.get('districts_field'):
            self.districts_field = int(self.request.GET.get('districts_field'))
            # print(self.districts_field)
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field'))
            # print(self.blocks_field)
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
            # print(self.categories_field)
        if self.request.GET.get('management_field'):
            self.management_field = self.request.GET.get('management_field')
            # print(self.management_field)
        return super(SchoolList, self).get(request, *args, **kwargs)
    
    def get_initial(self):
        if self.request.user.is_block_admin:
            self.districts_field = self.request.user.block.block_district.id
            self.blocks_field = self.request.user.block.id
        elif self.request.user.is_district_admin:
            self.districts_field = self.request.user.district.id
        initial_data = {
            'academic_year_field': self.academic_year_field,
            'districts_field': self.districts_field,
            'blocks_field': self.blocks_field,
            'categories_field': self.categories_field,
            'management_field': self.management_field
        }
        return initial_data
    
    def get_form_kwargs(self):
        form = super().get_form_kwargs()
        form['user'] = self.request.user
        return form

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        if self.districts_field:
            form.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks(self.districts_field)
        return form

    def get_context_data(self, **kwargs):
        school = SchoolProfile.objects.filter(
                academic_year = self.academic_year_field,
                sp_school__school_district = self.districts_field,
                sp_school__school_block = self.blocks_field,
               
        )
        # print(school)
        # print(self.categories_field)
        # print(self.management_field)
        if self.categories_field:
            school = school.filter(
                sp_school_category = self.categories_field,
                
            )
        elif self.management_field :
            school = school.filter(
                sp_management_code =self.management_field,
            )
        # print(school)
        if school:
            kwargs['school'] = school
            return super().get_context_data(**kwargs)
        else:
            kwargs['school'] = None
            return super().get_context_data(**kwargs)