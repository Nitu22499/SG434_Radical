from django import forms
from profiles.models import District, Block
from misc.utilities import get_districts

class ReportForm(forms.Form):
    report_districts = forms.ChoiceField()
    report_blocks = forms.ChoiceField()

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['report_districts'].choices = get_districts()
        self.fields['report_blocks'].choices = (('', '-----'), )

        # if 'report_districts' in self.data:
        #     try:
        #         district_id = int(self.data.get('report_districts'))
        #         self.fields['report_blocks'].queryset = Block.objects.filter(block_district_id=district_id).order_by('block_name')
        #     except (ValueError, TypeError):
        #         print("Exception")  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['report_blocks'].queryset = self.instance.block_district.block_set.order_by('block_name')
