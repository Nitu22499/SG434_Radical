from datetime import date as datetime_date

from django import forms
from django.utils.translation import gettext as _

from profiles.models import Subject, section_choices, District, Block, School
from .utils import ERROR_MESSAGES
from .validators import validate_no_future_date_form


def convert_future_date_today_if_future(date_value):
    if date_value > datetime_date.today():
        return datetime_date.today()
    return date_value


class StudentFetchForm(forms.Form):
    student_fetch_start_date = forms.DateField(
        initial=datetime_date.today(), label='Start date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    student_fetch_end_date = forms.DateField(
        initial=datetime_date.today(), label='End date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
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
            raise forms.ValidationError(**ERROR_MESSAGES['invalid_date_range'])

        return self.cleaned_data

    def clean_student_fetch_start_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_start_date'])

    def clean_student_fetch_end_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_end_date'])


class StudentAttendanceCreateForm(forms.Form):
    create_date = forms.DateField(
        initial=datetime_date.today(), label='Start date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(), label='Subject', widget=forms.Select(attrs={'class': 'form-control'})
    )
    section = forms.ChoiceField(
        choices=section_choices, label='Section', help_text=_('section/ division of class'), widget=forms.Select({
            'class': 'form-control'})
    )

    def clean_create_date(self):
        date = self.cleaned_data['create_date']
        validate_no_future_date_form(date)
        return date


class EmployeeFetchForm(forms.Form):
    employee_fetch_start_date = forms.DateField(initial=datetime_date.today(), label='Start date',
                                                widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    employee_fetch_end_date = forms.DateField(initial=datetime_date.today(), label='End date',
                                              widget=forms.DateInput(attrs={
                                                  'class': 'form-control', 'type': 'date'
                                              }))

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get('employee_fetch_start_date')
        end_date = self.cleaned_data.get('employee_fetch_end_date')

        if end_date < start_date:
            raise forms.ValidationError(**ERROR_MESSAGES['invalid_date_range'])

        return self.cleaned_data

    def clean_employee_fetch_start_date(self):
        # print(self.cleaned_data['employee_fetch_start_date'])
        return convert_future_date_today_if_future(self.cleaned_data['employee_fetch_start_date'])

    def clean_employee_fetch_end_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['employee_fetch_end_date'])


class EmployeeAttendanceCreateForm(forms.Form):
    create_date = forms.DateField(
        initial=datetime_date.today(), label='Start date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean_create_date(self):
        date = self.cleaned_data['create_date']
        validate_no_future_date_form(date)
        return date


class MyAttendanceFetchForm(forms.Form):
    student_fetch_start_date = forms.DateField(
        initial=datetime_date.today(), label='Start date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    student_fetch_end_date = forms.DateField(
        initial=datetime_date.today(), label='End date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(), label='Subject', widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(MyAttendanceFetchForm, self).__init__(*args, **kwargs)

        if student:
            self.fields['subject'].queryset = Subject.objects.filter(subject_class=student.stud_class)

    def clean(self):
        super().clean()
        start_date = self.cleaned_data['student_fetch_start_date']
        end_date = self.cleaned_data['student_fetch_end_date']

        if end_date < start_date:
            raise forms.ValidationError(**ERROR_MESSAGES['invalid_date_range'])

        return self.cleaned_data

    def clean_student_fetch_start_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_start_date'])

    def clean_student_fetch_end_date(self):
        return convert_future_date_today_if_future(self.cleaned_data['student_fetch_end_date'])


# authorities view forms

class BlockAdminAttendanceFetchForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    block = forms.IntegerField(widget=forms.HiddenInput(), label='')
    district = forms.IntegerField(widget=forms.HiddenInput(), label='')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(BlockAdminAttendanceFetchForm, self).__init__(*args, **kwargs)

        if request:
            user = request.user
            self.fields['school'].queryset = School.objects.filter(school_block=user.block)
            self.fields['block'].initial = user.block.id
            self.fields['district'].initial = user.block.block_district_id


class DistrictAdminAttendanceFetchForm(forms.Form):
    block = forms.ModelChoiceField(queryset=Block.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ), required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))
    district = forms.IntegerField(widget=forms.HiddenInput(), label='')

    class Meta:
        fields = ('block', 'school')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(DistrictAdminAttendanceFetchForm, self).__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['school'].queryset = School.objects.filter(school_district=user.district)
            self.fields['block'].queryset = Block.objects.filter(block_district=user.district)
            self.fields['district'].initial = user.district.id


class StateAdminAttendanceFetchForm(forms.Form):
    district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'},
    ), required=False)
    block = forms.ModelChoiceField(queryset=Block.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ), required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        fields = ('district', 'block', 'school')
