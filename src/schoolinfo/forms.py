from django import forms
from .models import SchoolProfile,PhysicalFacilities
from django.db import transaction
from misc.utilities import year_choices

class SchoolProfileForm(forms.ModelForm):

    class Meta:
        model = SchoolProfile
        exclude = ('sp_school', 'academic_year')

class PhysicalFacilitiesForm(forms.ModelForm):

    class Meta:
        model = PhysicalFacilities
        exclude = ('pf_school','academic_year')

class SectionHomeForm(forms.Form):
    academic_year_field = forms.ChoiceField(label='', widget=forms.Select(attrs={'class':'form-select'}))

    def __init__(self, *args, **kwargs):
        super(SectionHomeForm, self).__init__(*args, **kwargs)
        self.fields['academic_year_field'].choices = (('', 'Change Academic Year'), ) + year_choices()


        