from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import random
import datetime
from misc.utilities import year_choices
from profiles.models import Student, Employee, User, class_choices, section_choices, stream_choices, appointment_status_choices

from django.forms import Select

class Select(Select):
    def create_option(self, *args,**kwargs):
        option = super().create_option(*args,**kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = True

        return option

class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    stud_mother_name = forms.CharField(label = "Mother's Name", widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    gender = forms.CharField(label='', widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'DD/MM/YYYY'}))
    stud_class = forms.CharField(label='', widget=forms.Select(choices=class_choices, attrs={'class':'form-select'}))
    stud_section = forms.CharField(label='', required = False, widget=Select(choices=section_choices, attrs={'class':'form-select'}))
    stud_stream = forms.CharField(label='', required = False, widget=Select(choices=stream_choices, attrs={'class':'form-select'}))
    stud_rollno = forms.CharField(label = "Roll No.", widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    stud_parents_no_primary = forms.CharField(label = "Parents Ph.No.", widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    stud_parents_no_alternative = forms.CharField(label = "Parents Ph.No.(Alternative) ", widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    stud_admission_year = forms.ChoiceField(label = '', widget=Select(attrs={'class':'form-control'}))
    stud_disability = forms.CharField(label = 'Disability(if any)', required = False, widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    password1 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'SegY8bH4harr'}))
    password2 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'SegY8bH4harr'}))


    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ("first_name", "middle_name", "last_name", "date_of_birth", "gender", "stud_class", "stud_section", "stud_rollno")
        
    def clean_date_of_birth(self):
        try:
            datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
            return self.cleaned_data['date_of_birth']
        except:
            raise forms.ValidationError("Invalid Date")

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)
        years_choices = (('', 'Admission Year'), ) + year_choices()
        self.fields['stud_admission_year'].choices = years_choices
        self.fields['username'].initial = str(random.randint(3, 99999))
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user, stud_mother_name = self.cleaned_data['stud_mother_name'], stud_class = self.cleaned_data['stud_class'],
            stud_section = self.cleaned_data['stud_section'], stud_stream = self.cleaned_data['stud_stream'],
            stud_rollno = self.cleaned_data['stud_rollno'], stud_parents_no_primary = self.cleaned_data['stud_parents_no_primary'],
            stud_parents_no_alternative = self.cleaned_data['stud_parents_no_alternative'], stud_admission_year = self.cleaned_data['stud_admission_year'],
            stud_disability = self.cleaned_data['stud_disability']
        )
        return user

class EmployeeSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    gender = forms.CharField(label='', widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'DD/MM/YYYY'}))
    emp_designation = forms.CharField(label = 'Designation', widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
    emp_appointment_status = forms.CharField(label='', required = False, widget=Select(choices=appointment_status_choices, attrs={'class':'form-select'}))
    emp_joining_date = forms.CharField(label = 'Joining date', required = False, widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder':'DD/MM/YYYY'}))
    is_teacher = forms.BooleanField(label = 'Is Teacher', required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    password1 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'SegY8bH4harr'}))
    password2 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'SegY8bH4harr'}))


    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ("first_name", "middle_name", "last_name", "date_of_birth", "gender", "stud_class", "stud_section", "stud_rollno")

    def __init__(self, *args, **kwargs):
        super(EmployeeSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = str(random.randint(3, 99999))
        
    def clean_date_of_birth(self):
        try:
            datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
            return self.cleaned_data['date_of_birth']
        except:
            raise forms.ValidationError("Invalid Date")
    
    def clean_emp_joining_date(self):
        if len(self.cleaned_data['emp_joining_date']) > 1:
            try:
                datetime.datetime.strptime(self.cleaned_data['emp_joining_date'], '%d/%m/%Y').date()
                return self.cleaned_data['emp_joining_date']
            except:
                raise forms.ValidationError("Invalid Date")
        else:
            return self.cleaned_data['emp_joining_date']


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
        user.is_employee = True
        if self.cleaned_data['is_teacher']:
            user.is_teacher = True
        user.save()
        employee = Employee.objects.create(user=user, emp_designation = self.cleaned_data['emp_designation'],
            emp_appointment_status = self.cleaned_data['emp_appointment_status'],
        )
        if len(self.cleaned_data['emp_joining_date']) > 1:
            employee.emp_joining_date = datetime.datetime.strptime(self.cleaned_data['emp_joining_date'], '%d/%m/%Y').date()
        employee.save()
        return user