from django import forms
from datetime import date
from django.utils.translation import gettext as _

from profiles.models import Subject, section_choices

error_messages = {
    'invalid_date_range': {'message': _('"Start date" cannot be future date of "end date"'),
                           'code': 'invalid_date_range'}
}


def convert_future_date_today_if_future(date_value):
    if date_value > date.today():
        return date.today()
    return date_value


class StudentFetchForm(forms.Form):
    student_fetch_start_date = forms.DateField(
        initial=date.today(), label='Start date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    student_fetch_end_date = forms.DateField(
        initial=date.today(), label='End date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(), label='Subject', widget=forms.Select(attrs={'class': 'form-control'})
    )
    section = forms.ChoiceField(
        choices=section_choices, label='Section', help_text=_('section/ division of class'), widget=forms.Select({
            'class': 'form-control'})
    )

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get('student_fetch_start_date')
        end_date = self.cleaned_data.get('student_fetch_end_date')

        if end_date < start_date:
            raise forms.ValidationError(**error_messages['invalid_date_range'])

        return self.cleaned_data

    def clean_student_fetch_start_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_start_date'])

    def clean_student_fetch_end_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_end_date'])


class EmployeeFetchForm(forms.Form):
    employee_fetch_start_date = forms.DateField(initial=date.today(), label='Start date',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    employee_fetch_end_date = forms.DateField(initial=date.today(), label='End date', widget=forms.DateInput(attrs={
        'class': 'form-control', 'type': 'date'
    }))

    error_messages = {
        'invalid_date_range': _('Start date cannot be future of end date')
    }

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get('employee_fetch_start_date')
        end_date = self.cleaned_data.get('employee_fetch_end_date')

        if end_date < start_date:
            raise forms.ValidationError(**error_messages['invalid_date_range'])

        return self.cleaned_data

    def clean_employee_fetch_start_date(self):
        print(self.cleaned_data['employee_fetch_start_date'])
        return convert_future_date_today_if_future(self.cleaned_data['employee_fetch_start_date'])

    def clean_employee_fetch_end_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['employee_fetch_end_date'])
