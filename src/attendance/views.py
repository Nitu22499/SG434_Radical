from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView

from .models import StudentAttendance, StudentAttendanceItem, EmployeeAttendance, EmployeeAttendanceItem


class AttendanceHomeView(TemplateView):
    template_name = 'attendance/attendance.html'


def mark_attendance(request, pk):
    if 'student' in request.path:
        attendance_item = StudentAttendanceItem.objects.filter(student_attendance_item_attendance_object_id=pk)
        attendance_item.filter(pk__in=request.POST.getlist('present')).update(student_attendance_item_is_present=True)
        attendance_item.exclude(pk__in=request.POST.getlist('present')).update(student_attendance_item_is_present=False)
        return redirect('attendance:student-detail', pk)

    elif 'employee' in request.path:
        attendance_item = EmployeeAttendanceItem.objects.filter(employee_attendance_item_attendance_object_id=pk)
        attendance_item.filter(pk__in=request.POST.getlist('present')).update(employee_attendance_item_is_present=True)
        attendance_item.exclude(pk__in=request.POST.getlist('present')).update(
            employee_attendance_item_is_present=False)
        return redirect('attendance:employee-detail', pk)
    redirect('attendance:home')


"""
Student attendance section
"""


class StudentAttendanceCreateView(CreateView):
    model = StudentAttendance
    template_name = 'attendance/student_attendance_create_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form = form.save()
        return redirect('attendance:student-update', form.id)


class StudentAttendanceUpdateView(TemplateView):
    template_name = 'attendance/student_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceUpdateView, self).get_context_data(**kwargs)
        context['attendance'] = StudentAttendance.objects.get(pk=context.get('pk'))
        context['students'] = StudentAttendanceItem.objects.filter(
            student_attendance_item_attendance_object_id=context.get('pk'))
        return context


class StudentAttendanceListView(ListView):
    model = StudentAttendance
    context_object_name = 'attendances'
    template_name = 'attendance/student_attendance_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentAttendanceListView, self).get_context_data(**kwargs)
        context['unique_dates'] = StudentAttendance.objects.values_list('student_attendance_date', flat=True).distinct()
        return context


class StudentAttendanceDetailView(DetailView):
    model = StudentAttendance
    context_object_name = 'attendance'
    template_name = 'attendance/student_attendance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAttendanceDetailView, self).get_context_data(**kwargs)
        context['students'] = StudentAttendanceItem.objects.filter(
            student_attendance_item_attendance_object_id=self.kwargs['pk'])
        return context


class StudentAttendanceDeleteView(DeleteView):
    model = StudentAttendance

    def get_success_url(self):
        return reverse('attendance:student-list')


"""
Employee attendance section
"""


class EmployeeAttendanceCreateView(CreateView):
    model = EmployeeAttendance
    template_name = 'attendance/employee_attendance_create_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form = form.save()
        return redirect('attendance:employee-update', form.id)


class EmployeeAttendanceUpdateView(TemplateView):
    template_name = 'attendance/employee_attendance_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeAttendanceUpdateView, self).get_context_data(**kwargs)
        context['attendance'] = EmployeeAttendance.objects.get(pk=context.get('pk'))
        context['employees'] = EmployeeAttendanceItem.objects.filter(
            employee_attendance_item_attendance_object_id=context.get('pk'))
        return context


class EmployeeAttendanceListView(ListView):
    model = EmployeeAttendance
    context_object_name = 'attendances'
    template_name = 'attendance/employee_attendance_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeAttendanceListView, self).get_context_data(**kwargs)
        context['unique_dates'] = EmployeeAttendance.objects.values_list('employee_attendance_date',
                                                                         flat=True).distinct()
        return context


class EmployeeAttendanceDetailView(DetailView):
    model = EmployeeAttendance
    context_object_name = 'attendance'
    template_name = 'attendance/employee_attendance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeAttendanceDetailView, self).get_context_data(**kwargs)
        context['employees'] = EmployeeAttendanceItem.objects.filter(
            employee_attendance_item_attendance_object_id=self.kwargs['pk'])
        return context


class EmployeeAttendanceDeleteView(DeleteView):
    model = EmployeeAttendance

    def get_success_url(self):
        return reverse('attendance:employee-list')
