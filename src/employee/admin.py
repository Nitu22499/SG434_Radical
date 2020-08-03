from django.contrib import admin

from .models import Employee, Teacher
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class TeacherResource(resources.ModelResource):

    class Meta:
        model = Teacher


class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource

class EmployeeResource(resources.ModelResource):

    class Meta:
        model = Employee


class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource



admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Teacher,TeacherAdmin)
