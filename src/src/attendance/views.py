from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, FormView

from attendance.forms import StudentFetchForm, EmployeeFetchForm, StudentAttendanceCreateForm, \
    EmployeeAttendanceCreateForm
from attendance.models import StudentAttendance, get_employee_attendance, EmployeeAttendance
from profiles.models import Student, Subject, User
from .models import get_student_attendance


class AttendanceIndexView(TemplateView):
    template_name = 'attendance/attendance.html'


def student_mark_attendance(request, create_date, subject, section):
    attendance_item = get_student_attendance(create_date, subject, section, request.user.school)
    attendance_item.filter(pk__in=request.POST.getlist('present')).update(student_attendance_is_present=True)
    attendance_item.exclude(pk__in=request.POST.getlist('present')).update(student_attendance_is_present=False)

    parameter = {
        'create_date': create_date,
        'subject': subject,
        'section': section
    }
    return redirect('attendance:student_detail', **parameter)


class StudentAttendanceListView(TemplateView):
    template_name = 'attendance/student_attendance_list.html'

    def get_context_data(self, **kwargs):
        date_header = StudentAttendance.objects.values_list(
            'student_attendance_date', flat=True
        ).order_by(
            'student_attendance_date'
        ).filter(
            student_attendance_date__range=(kwargs['start_date'], kwargs['end_date'])
        ).distinct()

        header = ['Roll no', 'First name', 'Last name', *date_header, 'present percent']

        subject = Subject.objects.get(pk=kwargs['subject'])

        students = Student.objects.values_list(
            'user__first_name', 'user__last_name', 'stud_rollno', 'pk'
        ).order_by(
            'stud_rollno'
        ).filter(
            stud_class=subject.subject_class, stud_section=kwargs['section'], stud_school=self.request.user.school
        ).distinct()

        field_value = []
        for first_name, last_name, stud_rollno, pk in students:
            attendance = StudentAttendance.objects.values_list(
                'student_attendance_is_present', flat=True
            ).order_by(
                'student_attendance_date'
            ).filter(
                student_attendance_date__range=(kwargs['start_date'], kwargs['end_date']),
                student_attendance_student_id=pk, student_attendance_subject_id=kwargs['subject']
            )

            try:
                present_percent = '{:.2f}'.format(list(attendance).count(True) / attendance.count() * 100)

            except ZeroDivisionError:
                present_percent = '--'

            field_value.append([stud_rollno, first_name, last_name, *attendance, present_percent])

        kwargs['header'] = header
        kwargs['field_values'] = field_value

        # info display inside template
        subject = Subject.objects.get(pk=kwargs['subject'])
        kwargs['display'] = {
            'start_date': datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class
        }

        return kwargs


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


class StudentAttendanceDetailView(TemplateView):
    template_name = 'attendance/student_attendance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceDetailView, self).get_context_data(**kwargs)

        context['attendance'] = get_student_attendance(context['create_date'], context['subject'], context['section'],
                                                       self.request.user.school)

        # info display inside template
        subject = Subject.objects.get(pk=context['subject'])
        context['display'] = {
            'date': datetime.strptime(context['create_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class
        }

        return context


class StudentAttendanceCreateView(FormView):
    template_name = 'attendance/student_attendance_create_form.html'
    form_class = StudentAttendanceCreateForm

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        school = self.request.user.school
        section = form.cleaned_data['section']
        create_date = form.cleaned_data['create_date']

        if get_student_attendance(create_date, subject, section, school).count():
            messages.warning(self.request, _('attendance for this date, subject, section already exist.'))
            return redirect('attendance:student_add')

        students = Student.objects.filter(
            stud_school=school,
            stud_class=subject.subject_class,
            stud_section=section
        )

        attendance_object_list = []

        for student in students:
            attendance_object_list.append(StudentAttendance(
                student_attendance_date=create_date,
                student_attendance_school=school,
                student_attendance_section=section,
                student_attendance_subject=subject,
                student_attendance_student=student
            ))

        StudentAttendance.objects.bulk_create(attendance_object_list)

        print(create_date, subject.pk, section, subject)
        parameters = {
            'create_date': create_date,
            'subject': subject.pk,
            'section': section,
        }
        return redirect('attendance:student_update', **parameters)


class StudentAttendanceUpdateView(TemplateView):
    template_name = 'attendance/student_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceUpdateView, self).get_context_data(**kwargs)
        context['attendance'] = get_student_attendance(context['create_date'], context['subject'], context['section'],
                                                       self.request.user.school)

        # to display information in the update view
        subject = Subject.objects.get(pk=context['subject'])
        context['display'] = {
            'date': datetime.strptime(context['create_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class,
        }

        return context


def student_attendance_delete_view(request):
    attendances = get_student_attendance(request.POST['create_date'], request.POST['subject'], request.POST['section'],
                                         request.user.school)
    attendances.delete()
    return redirect('attendance:student_home')


def employee_mark_attendance(request, create_date):
    attendance = get_employee_attendance(create_date, request.user.school)
    present_list = list(map(int, request.POST.getlist('present')))

    for attendance_item, reason in zip(attendance, request.POST.getlist('reason')):
        print(attendance_item.pk, present_list, attendance_item.pk in present_list)
        if attendance_item.pk in present_list:
            attendance_item.employee_attendance_is_present = True
            attendance_item.employee_attendance_reason_for_absence = ''
        else:
            attendance_item.employee_attendance_is_present = False

            if reason:
                attendance_item.employee_attendance_reason_for_absence = reason
            else:
                attendance_item.employee_attendance_reason_for_absence = "NA"
        attendance_item.save()

    parameter = {
        'create_date': create_date,
    }
    return redirect('attendance:employee_detail', **parameter)


class EmployeeAttendanceListView(TemplateView):
    template_name = 'attendance/employee_attendance_list.html'

    def get_context_data(self, **kwargs):
        date_header = EmployeeAttendance.objects.values_list(
            'employee_attendance_date', flat=True
        ).order_by(
            'employee_attendance_date'
        ).filter(
            employee_attendance_date__range=(kwargs['start_date'], kwargs['end_date'])
        ).distinct()

        header = ['First name', 'Last name', *date_header, 'Present percent']

        employees = User.objects.values_list(
            'first_name', 'last_name', 'pk'
        ).order_by(
            'first_name', 'last_name'
        ).filter(
            is_employee=True
        ).distinct()

        field_value = []
        for first_name, last_name, pk in employees:
            attendance = EmployeeAttendance.objects.values_list(
                'employee_attendance_is_present', flat=True
            ).order_by(
                'employee_attendance_date'
            ).filter(
                employee_attendance_date__range=(kwargs['start_date'], kwargs['end_date']),
                employee_attendance_employee_id=pk,
            )

            try:
                present_percent = '{:.2f}'.format(list(attendance).count(True) / attendance.count() * 100)

            except ZeroDivisionError:
                present_percent = '--'

            field_value.append([first_name, last_name, *attendance, present_percent])

        kwargs['header'] = header
        kwargs['field_values'] = field_value

        # info display inside template
        kwargs['display'] = {
            'start_date': datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date(),
        }

        return kwargs


class EmployeeAttendanceHomeView(FormView):
    form_class = EmployeeFetchForm
    template_name = 'attendance/employee_attendance_home.html'

    def form_valid(self, form):
        parameter = {
            'start_date': str(form.cleaned_data.get('employee_fetch_start_date')),
            'end_date': str(form.cleaned_data.get('employee_fetch_end_date')),
        }

        dates = EmployeeAttendance.objects.values_list(
            'employee_attendance_date', flat=True
        ).order_by(
            'employee_attendance_date'
        ).filter(
            employee_attendance_date__range=(parameter['start_date'], parameter['end_date'])
        ).distinct()

        if not dates.count():
            messages.warning(self.request, _(
                f"There is no attendance record between {parameter['start_date']} - {parameter['end_date']}"))
            return redirect('attendance:employee_home')

        return redirect('attendance:employee_view', **parameter)


class EmployeeAttendanceDetailView(TemplateView):
    template_name = 'attendance/employee_attendance_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['attendance'] = get_employee_attendance(kwargs['create_date'], self.request.user.school)

        # info display inside template
        kwargs['display'] = {
            'date': datetime.strptime(kwargs['create_date'], '%Y-%m-%d').date(),
        }

        return kwargs


class EmployeeAttendanceCreateView(FormView):
    template_name = 'attendance/employee_attendance_create_form.html'
    form_class = EmployeeAttendanceCreateForm

    def form_valid(self, form):
        school = self.request.user.school
        create_date = form.cleaned_data['create_date']

        # todo add school when employee has that
        employees = User.objects.filter(
            is_employee=True,
        )

        if get_employee_attendance(create_date, school).count():
            messages.warning(self.request, _(f'Attendance for {create_date} already exist.'))
            return redirect('attendance:employee_add')

        attendance_object_list = []

        for employee in employees:
            attendance_object_list.append(EmployeeAttendance(
                employee_attendance_date=create_date,
                employee_attendance_school=school,
                employee_attendance_employee=employee
            ))

        EmployeeAttendance.objects.bulk_create(attendance_object_list)

        # todo add school when employee has that
        parameters = {
            'create_date': create_date,
        }
        return redirect('attendance:employee_update', **parameters)


class EmployeeAttendanceUpdateView(TemplateView):
    template_name = 'attendance/employee_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        kwargs['attendance'] = get_employee_attendance(kwargs['create_date'], self.request.user.school)

        # to display information in the update view
        kwargs['display'] = {
            'date': datetime.strptime(kwargs['create_date'], '%Y-%m-%d').date(),
        }

        return kwargs


def employee_attendance_delete_view(request):
    attendances = get_employee_attendance(request.POST['create_date'], request.user.school)
    attendances.delete()
    return redirect('attendance:employee_home')
