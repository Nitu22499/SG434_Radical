# Generated by Django 3.0.8 on 2020-08-01 04:09

import attendance.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_attendance_date', models.DateField(default=django.utils.timezone.now, validators=[attendance.validators.validate_no_future_date], verbose_name='Date')),
                ('employee_attendance_is_present', models.BooleanField(default=False, verbose_name='is present')),
                ('employee_attendance_reason_for_absence', models.CharField(default='', max_length=500, verbose_name='Reason for absence')),
            ],
            options={
                'ordering': ['-employee_attendance_date', 'employee_attendance_employee__employee_user__first_name', 'employee_attendance_employee__employee_user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_attendance_date', models.DateField(default=django.utils.timezone.now, validators=[attendance.validators.validate_no_future_date], verbose_name='Date')),
                ('student_attendance_section', models.CharField(choices=[('', 'SECTION'), ('NA', 'NA'), ('A', 'SECTION A'), ('B', 'SECTION B'), ('C', 'SECTION C'), ('D', 'SECTION D'), ('E', 'SECTION E'), ('F', 'SECTION F')], help_text='section/ division of the students', max_length=50, verbose_name='section')),
                ('student_attendance_is_present', models.BooleanField(default=False, verbose_name='is present')),
            ],
            options={
                'ordering': ['-student_attendance_date', 'student_attendance_subject', 'student_attendance_student__stud_rollno'],
            },
        ),
    ]
