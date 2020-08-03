from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, FormView

from attendance.forms import (
    StudentFetchForm, EmployeeFetchForm, StudentAttendanceCreateForm, EmployeeAttendanceCreateForm,
    MyAttendanceFetchForm, StateAdminAttendanceFetchForm, DistrictAdminAttendanceFetchForm,
    BlockAdminAttendanceFetchForm
)
from attendance.models import StudentAttendance, get_employee_attendance, EmployeeAttendance, get_my_attendance
from employee.models import Employee
from profiles.models import Student, Subject, School, Block
from .models import get_student_attendance, get_student_attendance_dates


class AttendanceIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/attendance.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_student:
            return redirect('attendance:my_home')
        else:
            return super(AttendanceIndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        location = None
        authority_type = None
        if self.request.user.is_school_admin:
            location = self.request.user.school
            authority_type = 'School Admin'
        elif self.request.user.is_block_admin:
            location = self.request.user.block
            authority_type = 'Block Admin'
        elif self.request.user.is_district_admin:
            location = self.request.user.district
            authority_type = 'District Admin'
        elif self.request.user.is_state_admin:
            location = 'Sikkim'
            authority_type = 'State Admin'

        kwargs['display'] = {
            'location': location,
            'authority_type': authority_type
        }

        return kwargs


"""
Student from authority perspective
"""


@login_required()
def student_mark_attendance(request, create_date, subject, section):
    attendance_item = get_student_attendance(create_date, subject, section, request.user.school)
    attendance_item.filter(pk__in=request.POST.getlist('present')).update(student_attendance_is_present=True)
    attendance_item.exclude(pk__in=request.POST.getlist('present')).update(student_attendance_is_present=False)

    parameter = {
        'create_date': create_date,
        'subject': subject,
        'section': section,
        'school': request.user.school.id
    }
    return redirect('attendance:student_detail', **parameter)


class StudentAttendanceListView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/student_attendance_list.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        school = None
        if self.request.user.is_school_admin:
            school = self.request.user.school
        elif self.request.user.is_employee:
            school = Employee.objects.get(employee_user=self.request.user).employee_school
        elif not self.request.user.is_student:
            school = School.objects.get(pk=kwargs['school'])

        date_header = get_student_attendance_dates(kwargs['start_date'], kwargs['end_date'], kwargs['subject'],
                                                   kwargs['section'], school)

        header = ['Roll no', 'Full name', *date_header, 'present percent']

        subject = Subject.objects.get(pk=kwargs['subject'])

        students = Student.objects.values_list(
            'user__first_name', 'user__last_name', 'stud_rollno', 'pk'
        ).order_by(
            'stud_rollno'
        ).filter(
            stud_class=subject.subject_class, stud_section=kwargs['section'], stud_school=school
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

            field_value.append([stud_rollno, f'{first_name} {last_name}', *attendance, present_percent])

        kwargs['header'] = header
        kwargs['field_values'] = field_value
        kwargs['school'] = school.id

        # info display inside template
        subject = Subject.objects.get(pk=kwargs['subject'])
        kwargs['display'] = {
            'start_date': datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class
        }

        return kwargs


class StudentAttendanceHomeView(LoginRequiredMixin, FormView):
    form_class = StudentFetchForm
    template_name = 'attendance/student_attendance_home.html'

    # noinspection DuplicatedCode
    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceHomeView, self).get_context_data(**kwargs)
        context['authority_form'] = None

        if self.request.user.is_state_admin:
            context['authority_form'] = StateAdminAttendanceFetchForm
        elif self.request.user.is_district_admin:
            context['authority_form'] = DistrictAdminAttendanceFetchForm(request=self.request)
        elif self.request.user.is_block_admin:
            context['authority_form'] = BlockAdminAttendanceFetchForm(request=self.request)
        return context

    def form_valid(self, form):
        school = None
        if self.request.user.is_school_admin:
            school = self.request.user.school
        elif self.request.user.is_employee:
            logged_in_employee = Employee.objects.get(employee_user=self.request.user)
            school = logged_in_employee.employee_school
        elif not self.request.user.is_student:
            school = School.objects.get(id=self.request.POST.get('school'))

        parameter = {
            'start_date': str(form.cleaned_data.get('student_fetch_start_date')),
            'end_date': str(form.cleaned_data.get('student_fetch_end_date')),
            'subject': form.cleaned_data.get('subject').pk,
            'section': form.cleaned_data.get('section'),
            'school': school.id
        }
        section = parameter['section'] if parameter['section'] != 'NA' else ''

        date = get_student_attendance_dates(parameter['start_date'], parameter['end_date'], parameter['subject'],
                                            parameter['section'], school)

        if not date.count():
            messages.warning(
                self.request, _(
                    f"There is no attendance record between {parameter['start_date']} -\
                     {parameter['end_date']} for class {form.cleaned_data['subject'].subject_class} {section} and\
                      subject: {form.cleaned_data['subject'].subject_name}"
                ))
            return redirect('attendance:student_home')
        return redirect('attendance:student_view', **parameter)


class StudentAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/student_attendance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceDetailView, self).get_context_data(**kwargs)

        context['attendance'] = get_student_attendance(context['create_date'], context['subject'], context['section'],
                                                       context['school'])

        # info display inside template
        subject = Subject.objects.get(pk=context['subject'])
        context['display'] = {
            'date': datetime.strptime(context['create_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class
        }

        return context


class StudentAttendanceCreateView(LoginRequiredMixin, FormView):
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


class StudentAttendanceUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/student_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceUpdateView, self).get_context_data(**kwargs)
        context['attendance'] = get_student_attendance(context['create_date'], context['subject'], context['section'],
                                                       self.request.user.school)
        context['school'] = self.request.user.school.id
        print(context['school'])

        # to display information in the update view
        subject = Subject.objects.get(pk=context['subject'])
        context['display'] = {
            'date': datetime.strptime(context['create_date'], '%Y-%m-%d').date(),
            'subject': subject.subject_name,
            'class': subject.subject_class,
        }

        return context


class StudentAttendanceIdView(LoginRequiredMixin, FormView):
    template_name = 'attendance/student_attendance_individual.html'
    form_class = MyAttendanceFetchForm

    def get(self, request, *args, **kwargs):
        if not Student.objects.filter(pk=kwargs['pk']).exists():
            raise Http404(_('Student Does not exist'))
        return super(StudentAttendanceIdView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceIdView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(StudentAttendanceIdView, self).get_form_kwargs()
        student = Student.objects.get(pk=self.kwargs['pk'])
        kwargs['student'] = student
        return kwargs

    def form_valid(self, form):
        student = Student.objects.get(pk=self.kwargs['pk'])

        attendance = get_my_attendance(form.cleaned_data['student_fetch_start_date'],
                                       form.cleaned_data['student_fetch_end_date'], form.cleaned_data['subject'],
                                       student.stud_section, student.stud_school, student)

        if not attendance.count():
            messages.warning(self.request, 'No classes found between these dates')
            return redirect('attendance:student_id', pk=student.id)

        parameters = {
            'student': student.id,
            'start_date': form.cleaned_data['student_fetch_start_date'],
            'end_date': form.cleaned_data['student_fetch_end_date'],
            'subject': form.cleaned_data['subject'].pk
        }

        return redirect('attendance:student_id_detail', **parameters)


@login_required()
def student_attendance_delete_view(request):
    attendances = get_student_attendance(request.POST['create_date'], request.POST['subject'], request.POST['section'],
                                         request.user.school)
    attendances.delete()
    return redirect('attendance:student_home')


"""
Employee from authority perspective
"""


@login_required()
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
        'school': request.user.school.id
    }
    return redirect('attendance:employee_detail', **parameter)


class EmployeeAttendanceListView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/employee_attendance_list.html'

    def get_context_data(self, **kwargs):
        date_header = EmployeeAttendance.objects.values_list(
            'employee_attendance_date', flat=True
        ).order_by(
            'employee_attendance_date'
        ).filter(
            employee_attendance_date__range=(kwargs['start_date'], kwargs['end_date']),
            employee_attendance_school_id=kwargs['school']
        ).distinct()

        header = ['Full name', *date_header, 'Present percent']

        school = None
        if self.request.user.is_employee:
            school = Employee.objects.get(employee_user=self.request.user).employee_school
        if self.request.user.is_school_admin:
            school = self.request.user.school
        if not self.request.user.is_student:
            school = School.objects.get(pk=kwargs['school'])

        employees = Employee.objects.values_list(
            'employee_user__first_name', 'employee_user__last_name', 'pk'
        ).order_by(
            'employee_user__last_name', 'employee_user__last_name'
        ).filter(
            employee_school=school
        )

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

            field_value.append([f'{first_name} {last_name}', *attendance, present_percent])

        kwargs['header'] = header
        kwargs['field_values'] = field_value

        # info display inside template
        kwargs['display'] = {
            'start_date': datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date(),
        }

        return kwargs


class EmployeeAttendanceHomeView(LoginRequiredMixin, FormView):
    form_class = EmployeeFetchForm
    template_name = 'attendance/employee_attendance_home.html'

    # noinspection DuplicatedCode
    def get_context_data(self, **kwargs):
        context = super(EmployeeAttendanceHomeView, self).get_context_data(**kwargs)
        context['authority_form'] = None

        if self.request.user.is_state_admin:
            context['authority_form'] = StateAdminAttendanceFetchForm
        elif self.request.user.is_district_admin:
            context['authority_form'] = DistrictAdminAttendanceFetchForm(request=self.request)
        elif self.request.user.is_block_admin:
            context['authority_form'] = BlockAdminAttendanceFetchForm(request=self.request)
        return context

    def form_valid(self, form):

        school = None
        if self.request.user.is_school_admin:
            school = self.request.user.school
        elif self.request.user.is_employee:
            logged_in_employee = Employee.objects.get(employee_user=self.request.user)
            school = logged_in_employee.employee_school
        elif not self.request.user.is_student:
            school = School.objects.get(id=self.request.POST.get('school'))

        parameter = {
            'start_date': str(form.cleaned_data.get('employee_fetch_start_date')),
            'end_date': str(form.cleaned_data.get('employee_fetch_end_date')),
            'school': school.id
        }

        dates = EmployeeAttendance.objects.values_list(
            'employee_attendance_date', flat=True
        ).order_by(
            'employee_attendance_date'
        ).filter(
            employee_attendance_date__range=(parameter['start_date'], parameter['end_date']),
            employee_attendance_school=school
        ).distinct()

        if not dates.count():
            messages.warning(self.request, _(
                f"There is no attendance record between {parameter['start_date']} - {parameter['end_date']}"))
            return redirect('attendance:employee_home')

        return redirect('attendance:employee_view', **parameter)


class EmployeeAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/employee_attendance_detail.html'

    def get_context_data(self, **kwargs):
        kwargs['attendance'] = get_employee_attendance(kwargs['create_date'], kwargs['school'])

        # info display inside template
        kwargs['display'] = {
            'date': datetime.strptime(kwargs['create_date'], '%Y-%m-%d').date(),
        }

        return kwargs


class EmployeeAttendanceCreateView(LoginRequiredMixin, FormView):
    template_name = 'attendance/employee_attendance_create_form.html'
    form_class = EmployeeAttendanceCreateForm

    def form_valid(self, form):
        school = self.request.user.school
        create_date = form.cleaned_data['create_date']

        employees = Employee.objects.filter(
            employee_school=school
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

        parameters = {
            'create_date': create_date,
        }
        return redirect('attendance:employee_update', **parameters)


class EmployeeAttendanceUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/employee_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        kwargs['attendance'] = get_employee_attendance(kwargs['create_date'], self.request.user.school)

        # to display information in the update view
        kwargs['display'] = {
            'date': datetime.strptime(kwargs['create_date'], '%Y-%m-%d').date(),
        }
        kwargs['school'] = self.request.user.school.id

        return kwargs


@login_required()
def employee_attendance_delete_view(request):
    attendances = get_employee_attendance(request.POST['create_date'], request.user.school)
    attendances.delete()
    return redirect('attendance:employee_home')


"""
Student from their perspective
"""


class MyAttendanceFetchView(LoginRequiredMixin, FormView):
    form_class = MyAttendanceFetchForm
    template_name = 'attendance/my_attendance_home.html'

    def form_valid(self, form):
        student = self.request.user.student

        attendance = get_my_attendance(form.cleaned_data['student_fetch_start_date'],
                                       form.cleaned_data['student_fetch_end_date'], form.cleaned_data['subject'],
                                       student.stud_section, student.stud_school, student)

        if not attendance.count():
            messages.warning(self.request, 'No classes found between these dates')
            return redirect('attendance:my_home')

        parameters = {
            'start_date': form.cleaned_data['student_fetch_start_date'],
            'end_date': form.cleaned_data['student_fetch_end_date'],
            'subject': form.cleaned_data['subject'].pk
        }

        return redirect('attendance:my_detail', **parameters)


class MyAttendanceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/my_attendance_detail.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_student:
            student = self.request.user.student
        else:
            student = Student.objects.get(pk=self.kwargs['student'])

        print(student)

        # info display inside template
        kwargs['display'] = {
            'start_date': datetime.strptime(kwargs['start_date'], '%Y-%m-%d').date(),
            'end_date': datetime.strptime(kwargs['end_date'], '%Y-%m-%d').date(),
            'subject': Subject.objects.get(pk=kwargs['subject']).subject_name,
            'student': student,
        }

        kwargs['attendance'] = get_my_attendance(kwargs['start_date'], kwargs['end_date'], kwargs['subject'],
                                                 student.stud_section, student.stud_school, student)

        # attendance stat footer info
        total = kwargs['attendance'].count()
        present = kwargs['attendance'].filter(student_attendance_is_present=True).count()
        absent = total - present

        try:
            present_percent = '{:.2f}'.format(present / total * 100)
        except ZeroDivisionError:
            present_percent = '--'

        kwargs['attendance_stat'] = {
            'present': present,
            'absent': absent,
            'total': total,
            'present_percent': present_percent
        }

        return kwargs


# authority fetch view data loads
def load_school(request):
    data_type = request.GET.get('data_type')
    block_id = request.GET.get('block_id')
    district_id = request.GET.get('district_id')
    schools = School.objects.all()

    if data_type == 'district' and district_id:
        schools = School.objects.filter(school_district_id=district_id)
    elif data_type == 'block':
        if block_id:
            schools = School.objects.filter(school_block_id=block_id)
        elif district_id:
            schools = School.objects.filter(school_district_id=district_id)

    print(schools)

    return render(request, 'attendance/dropdown_list_options.html', {'type': 'school', 'schools': schools})


def load_block(request):
    district_id = request.GET.get('district_id')
    blocks = Block.objects.all()
    if district_id:
        blocks = Block.objects.filter(block_district_id=district_id)

    return render(request, 'attendance/dropdown_list_options.html', {'type': 'block', 'blocks': blocks})
