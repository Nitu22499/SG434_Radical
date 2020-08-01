from django import forms

from attendance.models import StudentAttendance, EmployeeAttendance


class StudentAttendanceCreateForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        exclude = ('student_attendance_school',)

        widgets = {
            'student_attendance_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'student_attendance_section': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'student_attendance_subject': forms.Select(
                attrs={'class': 'form-control'}
            )
        }


class EmployeeAttendanceCreateForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendance
        exclude = ('employee_attendance_school',)

        widgets = {'employee_attendance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}
