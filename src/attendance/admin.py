from django.contrib import admin

from .models import StudentAttendance, StudentAttendanceItem, EmployeeAttendance, EmployeeAttendanceItem


# Register your models here.
class StudentAttendanceInline(admin.TabularInline):
    model = StudentAttendanceItem
    extra = 0
    can_delete = False
    verbose_name_plural = 'students'
    verbose_name = 'student'

    fields = ('full_name', 'student_attendance_item_is_present')
    readonly_fields = ('student_attendance_item_student', 'full_name')

    # pycharm linting warning suppressor
    # noinspection PyMethodMayBeStatic
    def full_name(self, obj):
        return obj.student_attendance_item_student.user.get_full_name()

    # to prevent accidentally adding someone
    def has_add_permission(self, request, obj):
        return False


class StudentAttendanceAdmin(admin.ModelAdmin):
    inlines = (StudentAttendanceInline,)
    list_display = ('__str__', 'student_attendance_date')

    # this line is to prevent showing empty student list when instance not already created
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(StudentAttendanceAdmin, self).get_inline_instances(request, obj)


class EmployeeAttendanceInline(admin.TabularInline):
    model = EmployeeAttendanceItem
    extra = 0
    can_delete = False
    verbose_name_plural = 'employees'
    verbose_name = 'employee'

    fields = ('full_name', 'employee_attendance_item_is_present')
    readonly_fields = ('employee_attendance_item_employee', 'full_name')

    # noinspection PyMethodMayBeStatic
    def full_name(self, obj):
        return obj.employee_attendance_item_employee.user.get_full_name()

    # to prevent accidentally adding someone
    def has_add_permission(self, request, obj):
        return False


class EmployeeAttendanceAdmin(admin.ModelAdmin):
    inlines = (EmployeeAttendanceInline,)

    # this line is to prevent showing empty employee list when instance not already created
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(EmployeeAttendanceAdmin, self).get_inline_instances(request, obj)


admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(EmployeeAttendance, EmployeeAttendanceAdmin)
