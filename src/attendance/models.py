from django.db import models
from django.utils.timezone import now as today_date
from django.utils.translation import gettext as _

from profiles.models import Student, Subject, section_choices, School, User
from .validators import validate_no_future_date


class StudentAttendance(models.Model):
    """model for individual student attendance

    This model generate student attendance record which is unique for
    each (date, subject, class, section, school). Due to the nature of
    this implementation there is no way to distinguish two separate
    type class occurred in same day for same subject.
    """
    student_attendance_date = models.DateField(_('Date'), default=today_date, validators=(validate_no_future_date,))
    student_attendance_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,
                                                   related_name='attendance', verbose_name=_('Subject'))
    student_attendance_section = models.CharField(max_length=50, choices=section_choices, verbose_name=_('section'),
                                                  help_text='section/ division of the students')
    student_attendance_school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name=_('school'))
    student_attendance_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True,
                                                   verbose_name=_('Student'))
    student_attendance_is_present = models.BooleanField(_('is present'), default=False)

    class Meta:
        ordering = ['-student_attendance_date', 'student_attendance_subject']
        unique_together = ('student_attendance_date', 'student_attendance_subject', 'student_attendance_section',
                           'student_attendance_school', 'student_attendance_student')

    def __str__(self):
        return f'{self.student_attendance_date} {self.student_attendance_subject}'


def get_student_attendance(create_date, subject, section, school) -> StudentAttendance.objects.filter:
    return StudentAttendance.objects.filter(
        student_attendance_date=create_date,
        student_attendance_subject_id=subject,
        student_attendance_section=section,
        student_attendance_school=school
    )


class EmployeeAttendance(models.Model):
    """model for individual employee attendance

    This model generate employee attendance record which is unique for
    each (date, subject, class, section, school). Due to the nature of
    this implementation there is no way to distinguish two separate
    type class occurred in same day for same subject.
    """
    employee_attendance_date = models.DateField(_('Date'), default=today_date, validators=(validate_no_future_date,), )
    employee_attendance_school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name=_('school'))
    employee_attendance_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                                     verbose_name=_('Employee'), limit_choices_to={'is_employee': True})
    employee_attendance_is_present = models.BooleanField(_('is present'), default=False)
    employee_attendance_reason_for_absence = models.CharField(_('Reason for absence'), max_length=500, default='')

    class Meta:
        ordering = ['-employee_attendance_date', 'employee_attendance_employee__first_name',
                    'employee_attendance_employee__last_name']
        unique_together = ('employee_attendance_date', 'employee_attendance_school', 'employee_attendance_employee',)

    def __str__(self):
        return str(self.employee_attendance_date)


def get_employee_attendance(create_date, school) -> EmployeeAttendance.objects.filter:
    return EmployeeAttendance.objects.filter(
        employee_attendance_date=create_date,
        employee_attendance_school=school
    )
