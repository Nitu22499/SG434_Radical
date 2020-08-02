from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, ListView, DetailView, DeleteView
from django.utils.translation import gettext as _

from profiles.models import User
from .forms import EmployeeCreateForm, TeacherCreateForm
from .models import Teacher, Employee


class EmployeeCreateView(FormView):
    form_class = EmployeeCreateForm
    template_name = 'employee/employee_create_form.html'
    success_url = reverse_lazy('employee:add')

    def get_context_data(self, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Employee'
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
        return super().form_valid(form)


class TeacherCreateView(UpdateView):
    form_class = TeacherCreateForm
    model = Teacher
    template_name = 'employee/employee_create_form.html'
    success_url = reverse_lazy('employee:add')

    def get_context_data(self, **kwargs):
        context = super(TeacherCreateView, self).get_context_data(**kwargs)
        context['form_title'] = 'Teacher'
        return context

    def form_valid(self, form):
        messages.success(self.request, _('Teacher data updated successfully'))
        return super().form_valid(form)


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/employee_list.html'

    def get_queryset(self):
        return Employee.objects.filter(employee_school=self.request.user.school)


class EmployeeDetailView(DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        print(context)
        employee = context['employee']
        if employee.employee_user.is_teacher:
            context['teacher'] = employee.teacher
        print(context)

        return context


class EmployeeDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('employee:list')
