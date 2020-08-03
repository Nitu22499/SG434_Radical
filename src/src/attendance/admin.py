from django.contrib import admin

from .models import StudentAttendance, EmployeeAttendance


class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'student_attendance_date')


class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'employee_attendance_date')


admin.site.register(StudentAttendance, StudentAttendanceAdmin)
admin.site.register(EmployeeAttendance, EmployeeAttendanceAdmin)
