from random import randint

from django import forms
from django.utils.translation import gettext as _

from profiles.models import User
from . import choices
from .models import Employee, Teacher


class EmployeeCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'true'}))
    middle_name = forms.CharField()
    last_name = forms.CharField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=choices.GENDER)
    is_teacher = forms.BooleanField(initial=False, label='is Teacher?', required=False,
                                    help_text=_('Ticking this option will show you teaching related fields later.'))

    class Meta:
        model = Employee
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'employee_contact_number',
                  'employee_email_address', 'employee_social_category', 'employee_nature_of_appointment',
                  'employee_highest_academic_qualification', 'employee_date_of_joining', 'employee_disability',
                  'employee_is_married', 'is_teacher', 'employee_other_info')

        widgets = {
            'employee_date_of_joining': forms.DateInput(attrs={
                'type': 'date'
            }),
            'employee_contact_number': forms.TextInput(attrs={
                'type': 'tel'
            }),
            'employee_email_address': forms.EmailInput(attrs={
                'type': 'email', 'placeholder': 'johndoe@email.com'
            })
        }

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = User()

        user.username = f'emp_{randint(1000, 9999)}'
        user.set_password('Pass@123')
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.gender = self.cleaned_data['gender']
        user.is_employee = True
        user.is_teacher = self.cleaned_data['is_teacher']
        user.save()

        employee.employee_user = user

        if commit:
            return employee.save()
        return employee


class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('teacher_employee',)
