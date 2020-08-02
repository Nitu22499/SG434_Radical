from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import random
import datetime
from misc.utilities import year_choices
from profiles.models import Student, User, class_choices, section_choices, religion_choices, socialCategory_choices, stream_choices,caste_choices,disability_choices


class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput())
    stud_mother_name = forms.CharField(label="Mother Name",widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'DD/MM/YYYY'}))
    stud_class = forms.CharField(label='Class', widget=forms.Select(choices=class_choices, attrs={'class':'form-select'}))
    stud_section = forms.CharField(label='Section', required = False, widget=forms.Select(choices=section_choices, attrs={'class':'form-select'}))
    stud_stream = forms.CharField(label='Stream', required = False, widget=forms.Select(choices=stream_choices, attrs={'class':'form-select'}))
    stud_rollno = forms.CharField(label = "Roll No.", widget=forms.TextInput())
    stud_socialCategory = forms.CharField(label='Social Category', required = False, widget=forms.Select(choices=socialCategory_choices, attrs={'class':'form-select'}))
    stud_caste = forms.CharField(label='Caste', required = False, widget=forms.Select(choices=caste_choices, attrs={'class':'form-select'}))
    stud_disability = forms.CharField(label='Disability', required = False, widget=forms.Select(choices=disability_choices, attrs={'class':'form-select'}))
    stud_religion = forms.CharField(label='Religion', required = False, widget=forms.Select(choices=religion_choices, attrs={'class':'form-select'}))
    stud_admissionDate = forms.CharField(label='Admission Date', widget=forms.TextInput(attrs={'placeholder':'DD/MM/YYYY'}))
    stud_address = forms.CharField(label='Address', widget=forms.TextInput())
    stud_parentContact = forms.IntegerField(label='Parents Contact No (Primary)', required=True, widget=forms.TextInput())
    stud_parentSecContact = forms.IntegerField(label='Parents Contact No (Secondary)', required=False, widget=forms.TextInput())
    password1 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'Pass@123'}))
    password2 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'Pass@123'}))


    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ("first_name", "middle_name", "last_name", "date_of_birth", "gender", "stud_class", "stud_section", "stud_rollno")
        
    def clean_date_of_birth(self):
        try:
            datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
            return self.cleaned_data['date_of_birth']
        except:
            raise forms.ValidationError("Invalid Date")

    def clean_admission_date(self):
        try:
            datetime.datetime.strptime(self.cleaned_data['stud_admissionDate'], '%d/%m/%Y').date()
            return self.cleaned_data['stud_admissionDate']
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
        student = Student(user=user, stud_mother_name = self.cleaned_data['stud_mother_name'],
            stud_class = self.cleaned_data['stud_class'],
            stud_section = self.cleaned_data['stud_section'],
            stud_rollno = self.cleaned_data['stud_rollno'], 
            stud_religion = self.cleaned_data['stud_religion'],
            stud_socialCategory = self.cleaned_data['stud_socialCategory'],
            stud_caste = self.cleaned_data['stud_caste'],
            stud_disability = self.cleaned_data['stud_disability'],
            stud_admissionDate = datetime.datetime.strptime(self.cleaned_data['stud_admissionDate'], '%d/%m/%Y').date(),
            stud_parentContact = self.cleaned_data['stud_parentContact'],
            stud_parentSecContact = self.cleaned_data['stud_parentSecContact'],
            stud_address = self.cleaned_data['stud_address'],
            
        )
        if commit == True:
            return user
        else:
            return student