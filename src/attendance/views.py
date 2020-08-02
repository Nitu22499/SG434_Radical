from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from attendance.forms import StudentFetchForm, EmployeeFetchForm


class AttendanceIndexView(TemplateView):
    template_name = 'attendance/attendance.html'


class StudentAttendanceView(TemplateView):
    template_name = 'attendance/student_attendance_detail.html'


class StudentAttendanceHomeView(FormView):
    form_class = StudentFetchForm
    template_name = 'attendance/student_attendance_home.html'

    def form_valid(self, form):
        parameter = {
            'start_date': str(form.cleaned_data.get('student_fetch_start_date')),
            'end_date': str(form.cleaned_data.get('student_fetch_end_date')),
            'subject': form.cleaned_data.get('subject').pk,
            'section': form.cleaned_data.get('section'),
        }
        return redirect('attendance:student_view', **parameter)


class EmployeeAttendanceView(TemplateView):
    template_name = 'attendance/employee_attendance_detail.html'


class EmployeeAttendanceHomeView(FormView):
    form_class = EmployeeFetchForm
    template_name = 'attendance/employee_attendance_home.html'

    def form_valid(self, form):
        parameter = {
            'start_date': str(form.cleaned_data.get('employee_fetch_start_date')),
            'end_date': str(form.cleaned_data.get('employee_fetch_end_date')),
        }
        return redirect('attendance:employee_view', **parameter)
