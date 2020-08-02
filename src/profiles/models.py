from django.contrib.auth.models import AbstractUser
from django.db import models

class_choices = (('1', 'CLASS 1'), ('2', 'CLASS 2'), ('3', 'CLASS 3'), ('4', 'CLASS 4'), ('5', 'CLASS 5'), ('6', 'CLASS 6'), ('7', 'CLASS 7'), ('8', 'CLASS 8'), ('9', 'CLASS 9'), ('10', 'CLASS 10'), ('11', 'CLASS 11'), ('12', 'CLASS 12'), ('LKG', 'LKG'), ('UKG', 'UKG'))
section_choices = (('', 'SECTION'), ('NA', 'NA'), ('A', 'SECTION A'), ('B', 'SECTION B'), ('C', 'SECTION C'), ('D', 'SECTION D'), ('E', 'SECTION E'), ('F', 'SECTION F'), )
stream_choices = (('', 'STREAM'), ('NA', 'NA'), ('COMMERCE', 'COMMERCE'), ('ELECTRICAL TECHNOLOGY', 'ELECTRICAL TECHNOLOGY'), ('HUMANITIES', 'HUMANITIES'), ('INFORMATION TECHNOLOGY', 'INFORMATION TECHNOLOGY'), ('PCM', 'PCM'), ('PCB', 'PCB'), ('TOURISM', 'TOURISM'))
district_choices = (('EAST SIKKIM', 'EAST SIKKIM'), ('WEST SIKKIM', 'WEST SIKKIM'), ('NORTH SIKKIM', 'NORTH SIKKIM'), ('SOUTH SIKKIM', 'SOUTH SIKKIM'))
board_choices = (('', 'Board'), ('NA', 'NA'), ('CBSE', 'CBSE'), ('State Board', 'State Board'), ('ICSE', 'ICSE'))
religion_choices = (('HINDU','HINDU'), ('MUSLIM','MUSLIM'), ('CHRISTIAN','CHRISTIAN'), ('SIKH','SIKH'), ('BUDDHIST', 'BUDDHIST'), ('PARSI','PARSI'), ('JAIN', 'JAIN'), ('OTHER','OTHER'))
socialCategory_choices = (('GENERAL','GENERAL'), ('SC','SC'), ('ST','ST'), ('OBC','OBC'), ('MBC', 'MBC'), ('OTHER','OTHER'))
caste_choices = (('RAI','RAI'),('BAHUN','BAHUN'),('SUBBA','SUBBA'),('TAMANG','TAMANG'),('KAMI','KAMI'),('CHHETRI','CHHETRI'),('LEPCHA','LEPCHA'),('GURUNG','GURUNG'),('PRADHAN','PRADHAN'),('MANGER','MANGER'),('DAMAI','DAMAI'),('LOHAR','LOHAR'),('BHUTIA','BHUTIA'),('KHAWAS','KHAWAS'),('OTHER','OTHER'))
disability_choices = (('NA','NA'),('BLINDNESS','BLINDNESS'),('LOW VISION','LOW VISION'),('HEARING IMPAIRMENT','HEARING IMPAIRMENT'),('SPEECH & LANGUAGE','SPEECH & LANGUAGE'),('LOCOMOTOR DISABILITY','LOCOMOTOR DISABILITY'),('MENTAL ILLNESS','MENTAL ILLNESS'),('SPECIFIC LEARNING DISABILITY','SPECIFIC LEARNING DISABILITY'),('CEREBRAL PALSY','CEREBRAL PALSY'),('AUTISM SPECTRUM DISORDER','AUTISM SPECTRUM DISORDER'),('MULTIPLE DISABILITY INCLUDING DEAF, BLINDNESS','MULTIPLE DISABILITY INCLUDING DEAF, BLINDNESS'),('LEPROSY CURED STUDENTS','LEPROSY CURED STUDENTS'),('DWARFISM','DWARFISM'),('INTELLECTUAL DISABILITY','INTELLECTUAL DISABILITY'),('MUSCULAR DYSTROPHY','MUSCULAR DYSTROPHY'),('CHRONIC NEUROLOGICAL COND','CHRONIC NEUROLOGICAL COND'),('MULTIPLE SCLEROSIS','MULTIPLE SCLEROSIS'),('THALASSEMIA','THALASSEMIA'),('HEMOPHILLIA','HEMOPHILLIA'),('SICKLE CELl DISEASE','SICKLE CELL DISEASE'),('ACID ATTACK VICTIM','ACID ATTACK VICTIM'),("PARKINSON's DISEASE","PARKINSON's DISEASE"))



class User(AbstractUser):
    middle_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField(max_length=10, default='Male', choices=(('Male', 'Male'), ('Female', 'Female')))
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_school_admin = models.BooleanField(default=False)
    is_block_admin = models.BooleanField(default=False)
    is_district_admin = models.BooleanField(default=False)
    is_state_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class District(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=250, choices=district_choices)
    
    def __str__(self):
        return self.district_name


class Block(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    block_name = models.CharField(max_length=250)
    block_district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.block_name



class School(models.Model):
    # school_code = 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=250)
    school_board = models.CharField(max_length=50, default = 'CBSE', choices=board_choices)
    school_block = models.ForeignKey(Block, on_delete=models.CASCADE)
    school_district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.school_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stud_mother_name=models.CharField(max_length=30, null = False,  default="")
    stud_class = models.CharField(max_length=5, choices=class_choices, blank=True)
    stud_section = models.CharField(max_length=5, choices=section_choices, default = 'NA', blank=True)
    stud_stream = models.CharField(max_length=25, choices=stream_choices, default = 'NA', blank=True)
    stud_rollno = models.CharField(max_length=10)
    stud_religion = models.CharField(max_length=15, choices=religion_choices, default = 'NA', blank=True)
    stud_socialCategory = models.CharField(max_length=10, choices=socialCategory_choices, default = 'NA', blank=True)
    stud_caste = models.CharField(max_length=10, choices=caste_choices, default = 'NA', blank=True)
    stud_disability = models.CharField(max_length=50, choices=disability_choices, default = 'NA', blank=True)
    stud_address = models.TextField(max_length=100, null = False,  default="")
    stud_admissionDate = models.DateField(null = True)
    stud_parentContact = models.IntegerField(null = True)
    stud_parentSecContact = models.IntegerField(null = True)
    stud_school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # teacher_id = 
    # teacher_school
    # teacher_subjects


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


    












