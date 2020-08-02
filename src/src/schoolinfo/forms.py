from django import forms
from .models import SchoolProfile,PhysicalFacilities
from django.db import transaction

class SchoolProfileForm(forms.ModelForm):

    class Meta:
        model = SchoolProfile
        exclude = ('sp_school', 'academic_year')

class PhysicalFacilitiesForm(forms.ModelForm):

    class Meta:
        model = PhysicalFacilities
        exclude = ('pf_school','academic_year')
        