from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import random
import datetime
from profiles.models import *
from misc.utilities import year_choices, get_districts, year_choices, get_blocks
from schoolinfo.models import school_category_code, SchoolProfile,management_school_code


class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput())
    stud_mother_name = forms.CharField(label="Mother Name",widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'DD/MM/YYYY'}))
    stud_class = forms.CharField(label='Class', widget=forms.Select(choices=class_choices, attrs={'class':'form-select','onchange':'manage()'}))
    stud_section = forms.CharField(label='Section', required = False, widget=forms.Select(choices=section_choices, attrs={'class':'form-select'}))
    stud_stream = forms.CharField(label='Stream', required = False, widget=forms.Select(choices=stream_choices, attrs={'class':'form-select','disabled':True}))
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
        if not self.cleaned_data['stud_stream']:
            self.cleaned_data['stud_stream']="NA"
        student = Student(user=user, stud_mother_name = self.cleaned_data['stud_mother_name'],
            stud_class = self.cleaned_data['stud_class'],
            stud_section = self.cleaned_data['stud_section'],
            stud_rollno = self.cleaned_data['stud_rollno'], 
            stud_stream = self.cleaned_data['stud_stream'], 
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


class SchoolSignUpForm(UserCreationForm):
    username = forms.CharField(label = '', widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    middle_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'DD/MM/YYYY'}))
    school_name = forms.CharField(widget=forms.TextInput())
    school_board = forms.CharField(label='Board', widget=forms.Select(choices=board_choices, attrs={'class':'form-select'}))
    school_district = forms.ModelChoiceField(label='District', queryset=District.objects.all())
    school_block = forms.ModelChoiceField(label='Block', queryset=Block.objects.none())
    school_cluster = forms.CharField(label='Cluster', widget=forms.TextInput())
    password1 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'Pass@123'}))
    password2 = forms.CharField(label = '', widget=forms.HiddenInput(attrs={'value':'Pass@123'}))

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ('user','school_name','school_board','school_block','school_district')
    
    def clean_date_of_birth(self):
        try:
            datetime.datetime.strptime(self.cleaned_data['date_of_birth'], '%d/%m/%Y').date()
            return self.cleaned_data['date_of_birth']
        except:
            raise forms.ValidationError("Invalid Date")

    def __init__(self, *args, **kwargs):
        super(SchoolSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = str(random.randint(3, 99999))
        # self.fields['school_block'].queryset = Block.objects.none()

        if 'school_district' in self.data:
            try:
                district_id = int(self.data.get('school_district'))
                self.fields['school_block'].queryset = Block.objects.filter(block_district=district_id).order_by('block_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['school_block'].queryset = self.instance.school.school_district.block_set.order_by('block_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_school_admin = True
        user.save()
        school_obj = School(user=user, school_name = self.cleaned_data['school_name'],
            school_board = self.cleaned_data['school_board'],
            school_district = self.cleaned_data['school_district'],
            school_block = self.cleaned_data['school_block'],
            school_cluster = self.cleaned_data['school_cluster'],            
        )
        if commit == True:
            return user
        else:
            return school_obj


class SchoolListForm(forms.Form):
    academic_year_field = forms.ChoiceField(label = 'Academic Year', required=True, widget=forms.Select(attrs={'class':'form-select'}))
    districts_field = forms.ChoiceField(label = 'District', required=True, widget=forms.Select(attrs={'class':'form-select'}))
    blocks_field = forms.ChoiceField(label='Block', required=True, widget=forms.Select(attrs={'class':'form-select'}))
    categories_field = forms.ChoiceField(label='Category', required=False, widget=forms.Select(attrs={'class':'form-select'}))
    management_field = forms.ChoiceField(label='Management', required=False, widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year_field'].choices = (('', 'Select Academic Year'), ) + year_choices()
        self.fields['districts_field'].choices = (('', 'Select District'), ) + get_districts()
        self.fields['blocks_field'].choices = (('', 'Select Block'), ) + get_blocks()
        self.fields['categories_field'].choices = (('', 'All'), ) + school_category_code
        self.fields['management_field'].choices = (('', 'All'), ) +  management_school_code
        
        if 'districts_field' in self.data:
            try:
                if self.data.get('districts_field'):
                    district_id = int(self.data.get('districts_field'))
                    self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks(district_id)
                else:
                    self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks()
            except (ValueError, TypeError):
                print("Exception") # invalid input from the client; ignore and fallback to empty City queryset