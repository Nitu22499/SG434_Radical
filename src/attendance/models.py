from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now as today_date
from django.utils.translation import gettext as _

from profiles.models import Student, Subject, section_choices


class StudentAttendance(models.Model):
    student_attendance_date = models.DateField(_('Date'), default=today_date)
    student_attendance_subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,
                                                   related_name='attendance', verbose_name=_('Subject'))
    student_attendance_section = models.CharField(max_length=50, choices=section_choices, verbose_name=_('section'),
                                                  help_text='section/ division of the students')

    # timestamps
    student_attendance_last_updated = models.DateTimeField(verbose_name=_('last updated'), auto_now=True)

    class Meta:
        unique_together = ('student_attendance_date', 'student_attendance_subject',)

    def __str__(self):
        return f'{self.student_attendance_date} {self.student_attendance_subject}'


class StudentAttendanceItem(models.Model):
    student_attendance_item_attendance_object = models.ForeignKey(StudentAttendance, on_delete=models.CASCADE,
                                                                  related_name='students',
                                                                  verbose_name=_('StudentAttendance Obj'))
    student_attendance_item_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True,
                                                        verbose_name=_('Student'))
    student_attendance_item_is_present = models.BooleanField(_('is present'), default=False)

    class Meta:
        unique_together = ('student_attendance_item_attendance_object', 'student_attendance_item_student')

    def __str__(self):
        return f'{self.student_attendance_item_student} {self.student_attendance_item_attendance_object}'


@receiver(post_save, sender=StudentAttendance)
def create_students_list_for_attendance(instance, created, **kwargs):
    if created:
        eligible_students_in_subject = Student.objects.filter(
            stud_section=instance.student_attendance_section,
            stud_class=instance.student_attendance_subject.subject_class
        )
        attendance_object_list = []
        for student in eligible_students_in_subject:
            attendance_object_list.append(StudentAttendanceItem(student_attendance_item_attendance_object=instance,
                                                                student_attendance_item_student=student))
        StudentAttendanceItem.objects.bulk_create(attendance_object_list)
