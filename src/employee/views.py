from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import FormView, UpdateView, ListView, DetailView, DeleteView

from attendance.forms import StateAdminAttendanceFetchForm, DistrictAdminAttendanceFetchForm, \
    BlockAdminAttendanceFetchForm
from profiles.models import User, School
from .forms import EmployeeCreateForm, TeacherCreateForm, EmployeeUpdateForm
from .models import Teacher, Employee


class EmployeeCreateView(LoginRequiredMixin, FormView):
    form_class = EmployeeCreateForm
    template_name = 'employee/employee_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['display'] = {
            'page_action': 'Add New',
            'form_title': 'Employee'
        }
        return context

    def form_valid(self, form):
        employee = form.save(commit=False)
        employee.employee_school = self.request.user.school
        employee.save()

        messages.success(self.request, _('Employee added successfully'))

        if form.cleaned_data['is_teacher']:
            teacher = Teacher(teacher_employee=employee)
            teacher.save()
            return redirect('employee:teacher_add', pk=teacher.id)
        return redirect('employee:detail', pk=employee.pk)


class TeacherCreateView(LoginRequiredMixin, UpdateView):
    form_class = TeacherCreateForm
    model = Teacher
    template_name = 'employee/employee_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherCreateView, self).get_context_data(**kwargs)
        context['display'] = {
            'page_action': 'Add new',
            'form_title': 'Teacher'
        }

        if 'update' in self.request.path.split('/'):
            context['display']['page_action'] = 'Update'
        return context

    def form_valid(self, form):
        teacher = form.save()
        messages.success(self.request, _('Teacher data updated successfully'))
        return redirect('employee:detail', teacher.teacher_employee_id)


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/employee_list.html'

    def get_queryset(self):
        if self.request.user.is_school_admin:
            return Employee.objects.filter(employee_school=self.request.user.school)
        elif self.request.user.is_employee:
            return Employee.objects.filter(employee_school=self.request.user.employee.employee_school)
        elif not self.request.user.is_student:
            return Employee.objects.filter(employee_school=self.kwargs['school'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeListView, self).get_context_data(object_list=object_list, **kwargs)

        context['school'] = None
        if self.request.user.is_school_admin:
            context['school'] = self.request.user.school
        elif self.request.user.is_employee:
            employee = Employee.objects.get(employee_user=self.request.user)
            context['school'] = employee.employee_school
        elif not self.request.user.is_student:
            context['school'] = School.objects.get(id=self.kwargs['school'])
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        employee = context['employee']
        if employee.employee_user.is_teacher:
            context['teacher'] = employee.teacher

        return context


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('employee:list')


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EmployeeUpdateForm
    model = Employee
    template_name = 'employee/employee_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeUpdateView, self).get_context_data(**kwargs)

        context['display'] = {
            'page_action': 'Update',
            'form_title': 'Employee'
        }

        return context

    def form_valid(self, form):
        form.save()
        return redirect('employee:detail', pk=self.object.pk)


class EmployeeAuthorityHomeView(LoginRequiredMixin, FormView):
    template_name = 'employee/employee_authority_form.html'
    form_class = StateAdminAttendanceFetchForm

    def get_form_class(self):
        if self.request.user.is_state_admin:
            return StateAdminAttendanceFetchForm
        elif self.request.user.is_district_admin:
            return DistrictAdminAttendanceFetchForm
        elif self.request.user.is_block_admin:
            return BlockAdminAttendanceFetchForm

    def get_form_kwargs(self):
        kwargs = super(EmployeeAuthorityHomeView, self).get_form_kwargs()
        if self.request.user.is_district_admin or self.request.user.is_block_admin:
            kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        print('hello world')
        print(type(form.cleaned_data['school']))
        return redirect('employee:list_with_school', school=form.cleaned_data['school'].id)
