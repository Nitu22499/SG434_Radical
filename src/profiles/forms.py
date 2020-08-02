from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import random
import datetime
from misc.utilities import year_choices
from profiles.models import Student, User, class_choices, section_choices


class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'DD/MM/YYYY'}))
    stud_class = forms.CharField(label='Class', widget=forms.Select(choices=class_choices, attrs={'class':'form-select'}))
    stud_section = forms.CharField(label='Section', required = False, widget=forms.Select(choices=section_choices, attrs={'class':'form-select'}))
    stud_rollno = forms.CharField(label = "Roll No.", widget=forms.TextInput())
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
        self.fields['username'].initial = str(random.randint(3, 99999))
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
        user.is_student = True
        user.save()
        student = Student(user=user, stud_class = self.cleaned_data['stud_class'],
            stud_section = self.cleaned_data['stud_section'],
            stud_rollno = self.cleaned_data['stud_rollno'], 
        )
        if commit == True:
            return user
        else:
            return student