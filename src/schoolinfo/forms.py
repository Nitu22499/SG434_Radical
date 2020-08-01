from django import forms
from .models import SchoolProfile
from .models import school_located_choices
from django.db import transaction

class SchoolProfileForm(forms.ModelForm):

    class Meta:
        model = SchoolProfile
        exclude = ('sp_school', 'academic_year')