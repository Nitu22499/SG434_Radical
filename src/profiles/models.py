from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    middle_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField(max_length=10, default='MALE', choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')))
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_school_admin = models.BooleanField(default=False)
    is_block_admin = models.BooleanField(default=False)
    is_district_admin = models.BooleanField(default=False)
    is_state_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class_choices = (('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'), ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'), ('LKG', 'LKG'), ('UKG', 'UKG'))
section_choices = (('', 'Section'), ('NA', 'NA'), ('A', 'Section A'), ('B', 'Section B'), ('C', 'Section C'), ('D', 'Section D'), ('E', 'Section E'), ('F', 'Section F'), )
stream_choices = (('', 'Stream'), ('NA', 'NA'), ('Commerce', 'Commerce'), ('Electrical Technology', 'Electrical Technology'), ('Humanities', 'Humanities'), ('Information Technology', 'Information Technology'), ('PCM', 'PCM'), ('PCB', 'PCB'), ('Tourism', 'Tourism'))
board_choices = (('', 'Board'), ('NA', 'NA'), ('CBSE', 'CBSE'), ('State Board', 'State Board'), ('ICSE', 'ICSE'))

class School(models.Model):
    # school_code = 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=250)
    school_board = models.CharField(max_length=50, default = 'CBSE', choices=board_choices)
    # school_brc = models.CharField(max_length=250, blank=True, choices=brc_choices)
    # school_crc = models.CharField(max_length=250, blank=True)
    # school_level = models.CharField(max_length=20, choices=school_level_choices)

    def __str__(self):
        return self.school_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # stud_id = models.AutoField()
    stud_class = models.CharField(max_length=5, choices=class_choices, blank=True)
    stud_section = models.CharField(max_length=5, choices=section_choices, default = 'NA', blank=True)
    stud_rollno = models.CharField(max_length=10)
    stud_mother_name = models.CharField(max_length=200, blank=True)
    stud_stream = models.CharField(max_length=30, choices=stream_choices, default = 'NA', blank=True)
    stud_parents_no_primary = models.CharField(max_length=15, blank = True)
    stud_parents_no_alternative = models.CharField(max_length=15, blank=True)
    stud_admission_year = models.CharField(max_length=20, blank=True)
    stud_disability = models.CharField(max_length=250, blank = True)
    stud_school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # teacher_id = 
    # teacher_school
    # teacher_subjects

appointment_status_choices = (('', 'Appointment Status'), ('Regular', 'Regular'), ('Temporary', 'Temporary'), ('Contract', 'Contract'))

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_designation = models.CharField(max_length=80, blank=True)
    emp_appointment_status = models.CharField(max_length=30, choices=appointment_status_choices, blank=True)
    emp_joining_date = models.DateField(null = True)
    # emp_teacher_subjects
    emp_school = models.ForeignKey(School, on_delete=models.CASCADE)
    # emp_id

    def __str__(self):
        return self.user.first_name

school_level_choices = (('', 'School Level'), ('PS', 'PS'), ('JHS', 'JHS'), ('SS', 'SS'), ('SSS', 'SSS'), ('Pre-Primary', 'Pre-Primary'))
subject_type_choices = (('Scholastic', 'Scholastic'), ('Co -Scholastic', 'Co -Scholastic'))
# JHS(upto Class 8), PS(Upto class 5)(same as LPS), SS(Upto class 10), SSS(Upto class 12)

# brc_choices = 

class Subject(models.Model):
    subject_board = models.CharField(max_length=100, blank=True, choices=board_choices, default='CBSE')
    subject_name = models.CharField(max_length=100, blank=True)
    subject_class = models.CharField(max_length=50, blank=True, choices=class_choices)
    subject_type = models.CharField(max_length=50, blank=True, choices=subject_type_choices)

    def __str__(self):
        return self.subject_class + " " + self.subject_name
    












