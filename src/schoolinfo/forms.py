from django import forms
from .models import *
from .models2 import *
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

class SchoolLibraryForm(forms.ModelForm):

    class Meta:
        model = SchoolLibrary
        exclude = ('sli_school_name','academic_year')    

class SchoolItemsForm(forms.ModelForm):

    class Meta:
        model = SchoolItems
        exclude = ('sit_school_name','academic_year')    

class SchoolToiletForm(forms.ModelForm):

    class Meta:
        model = SchoolToilet
        exclude = ('st_school_name','academic_year')


class SectionHomeForm(forms.Form):
    academic_year_field = forms.ChoiceField(label='', widget=forms.Select(attrs={'class':'form-select'}))

    def __init__(self, *args, **kwargs):
        super(SectionHomeForm, self).__init__(*args, **kwargs)
        self.fields['academic_year_field'].choices = (('', 'Change Academic Year'), ) + year_choices()

class SchoolSafetyForm(forms.ModelForm):

    class Meta:
        model = SchoolSafety
        exclude = ('sst_school_name','academic_year')

class SchoolReceiptForm(forms.ModelForm):

    class Meta:
        model = SchoolReceipt
        exclude = ('sre_school_name','academic_year')


