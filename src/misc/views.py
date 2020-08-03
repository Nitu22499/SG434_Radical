from django.views.generic import TemplateView
from profiles.models import District, Block
from django.shortcuts import render
from django.core.cache import cache
from .utilities import academic_year
from profiles.models import Student, School
from datetime import datetime
from django.utils import timezone
from employee.models import Employee

class LandingPage(TemplateView):
    template_name = 'misc/landing-page.html'


class Home(TemplateView):
    template_name = 'misc/landing-page.html'

    def get_template_names(self):
        if self.request.user.is_anonymous:
            return self.template_name

        if self.request.user.is_school_admin:
            self.template_name = 'misc/school_home.html'
            cache.set('last_synced', timezone.now(), None)
            cache.set('school_admin', self.request.user.school.pk, None)
        elif self.request.user.is_student:
            self.template_name = 'misc/student_home.html'
        elif self.request.user.is_block_admin:
            self.template_name = 'misc/block_home.html'
        elif self.request.user.is_district_admin:
            self.template_name = 'misc/district_home.html'
        return [self.template_name]

    def get_context_data(self, **kwargs):
        kwargs['academic_year'] = academic_year

        if self.request.user.is_anonymous:
            return super().get_context_data(**kwargs)

        if self.request.user.is_student:
            student = Student.objects.get(user=self.request.user)
            kwargs['student'] = student
        if self.request.user.is_school_admin:
            kwargs['students_count'] = Student.objects.count()
            kwargs['employees_count'] = Employee.objects.filter(employee_school = self.request.user.school).count()
        if self.request.user.is_block_admin:
            kwargs['schools_count'] = School.objects.filter(school_block = self.request.user.block).count()
            kwargs['employees_count'] = Employee.objects.filter(employee_school__school_block = self.request.user.block).count()
        
        if self.request.user.is_district_admin:
            kwargs['schools_count'] = School.objects.filter(school_district = self.request.user.district).count()
            kwargs['employees_count'] = Employee.objects.filter(employee_school__school_district = self.request.user.district).count()

        return super().get_context_data(**kwargs)


def load_blocks(request):
    district_id = request.GET.get('district')
    blocks = Block.objects.filter(block_district_id=district_id).order_by('block_name')
    return render(request, 'misc/block_dropdown_options.html', {'blocks': blocks})  
