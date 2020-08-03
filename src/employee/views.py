from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, ListView, DetailView, DeleteView
from django.utils.translation import gettext as _

from profiles.models import User
from .forms import EmployeeCreateForm, TeacherCreateForm, EmployeeUpdateForm
from .models import Teacher, Employee


class EmployeeCreateView(FormView):
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


class TeacherCreateView(UpdateView):
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


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/employee_list.html'

    def get_queryset(self):
        emp = Employee.objects.filter(employee_school=self.request.user.school)
        if emp:
            return emp
        return None


class EmployeeDetailView(DetailView):
    model = Employee
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        employee = context['employee']
        if employee.employee_user.is_teacher:
            context['teacher'] = employee.teacher

        return context


class EmployeeDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('employee:list')


class EmployeeUpdateView(UpdateView):
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
