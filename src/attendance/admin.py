from django.contrib import admin

from .models import StudentAttendance, StudentAttendanceItem


# Register your models here.
class StudentAttendanceInline(admin.TabularInline):
    model = StudentAttendanceItem
    extra = 0
    can_delete = False
    verbose_name_plural = 'students'
    verbose_name = 'student'

    # fieldsets = (None, {'fields': 'student_attendance_item_student', })

    fields = ('full_name', 'student_attendance_item_is_present')
    readonly_fields = ('student_attendance_item_student', 'full_name')

    # pycharm linting warning suppressor
    # noinspection PyMethodMayBeStatic
    def full_name(self, obj):
        return obj.student_attendance_item_student.user.get_full_name()

    # to prevent accidentally adding someone
    def has_add_permission(self, request, obj):
        return False


class AttendanceAdmin(admin.ModelAdmin):
    inlines = (StudentAttendanceInline,)
    readonly_fields = ('student_attendance_last_updated',)

    # this line is to prevent showing empty student list when instance not already created
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AttendanceAdmin, self).get_inline_instances(request, obj)


admin.site.register(StudentAttendance, AttendanceAdmin)
