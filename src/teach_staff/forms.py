from teach_staff.models import Teaching_Staff_NonTeachers_Info, Teaching_Staff_Info
from django import forms

class NonTeaching_Staff_Form(forms.ModelForm):

    class Meta:
        model = Teaching_Staff_NonTeachers_Info
        exclude = ('NonTeachers_School',)

class Teaching_Staff_Form(forms.ModelForm):

    class Meta:
        model = Teaching_Staff_Info
        exclude = ('Teacher_School',)
