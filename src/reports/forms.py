from django import forms
from profiles.models import District, Block
from misc.utilities import get_districts, year_choices, get_blocks
from schoolinfo.models import school_category_code

class ReportForm(forms.Form):
    academic_year_field = forms.ChoiceField(label = 'Academic Year', required=True, widget=forms.Select(attrs={'class':'form-select'}))
    districts_field = forms.ChoiceField(label = 'District', required=False, widget=forms.Select(attrs={'class':'form-select'}))
    blocks_field = forms.ChoiceField(label='Block', required=False, widget=forms.Select(attrs={'class':'form-select'}))
    categories_field = forms.ChoiceField(label='Category', required=False, widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year_field'].choices = year_choices()
        self.fields['districts_field'].choices = (('', 'All'), ) + get_districts()
        self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks()
        self.fields['categories_field'].choices = (('', 'All'), ) + school_category_code

        if 'districts_field' in self.data:
            try:
                if self.data.get('districts_field'):
                    district_id = int(self.data.get('districts_field'))
                    self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks(district_id)
                else:
                    self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks()
            except (ValueError, TypeError):
                print("Exception")  # invalid input from the client; ignore and fallback to empty City queryset
        # else:
        #     self.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks()
