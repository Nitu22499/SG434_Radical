from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from profiles.models import School
# Create your models here.

class Teaching_Staff_NonTeachers_Info(models.Model):
    NonTeachers_School = models.ForeignKey(School, on_delete = models.CASCADE)
    NonTeachers_Name = models.CharField(max_length = 25)

    NonTeachers_Gender = models.CharField(choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
    ), max_length = 30)

    NonTeachers_Date_of_birth = models.DateField()

    NonTeachers_Social_Category = models.CharField(choices = (
        ('OPEN', 'OPEN'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('ORC', 'ORC'),
        ('OTHERS', 'OTHERS'),
    ), max_length = 30)

    NonTeachers_Nature_Of_Appointment = models.CharField(choices = (
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('Part-Time', 'Part-Time')
    ), max_length = 30)

    NonTeachers_Date_of_Joining = models.DateField()
    NonTeachers_Joining_Year = models.IntegerField()

    NonTeachers_Disability = models.CharField(choices = (
        ('Not Applicable', 'Not Applicable'),
        ('Loco motor', 'Loco motor'),
        ('Visuals', 'Visuals'),
        ('Other', 'Other'),
        ('Hearing Impaired', 'Hearing Impaired'),
    ), max_length=50)

    NonTeacher_Qualifications = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate')
        
    ), max_length = 50)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    NonTeachers_Contact_Number = models.CharField(validators=[phone_regex], max_length=17)

    NonTeachers_Email = models.EmailField(max_length=254)

    def __str__(self):
        return self.NonTeachers_Name

    def get_absolute_url(self):
        return reverse("teach_staff:NonTeachers_Detail", kwargs={"pk": self.pk})
    
    NonTeachers_Other_Info = models.TextField(blank = True)




class Teaching_Staff_Info(models.Model):
    Teacher_School = models.ForeignKey(School, on_delete = models.CASCADE)

    Teacher_Code = models.CharField(max_length = 25, blank = True)
    Teacher_Name = models.CharField(max_length = 25)

    Teacher_Gender = models.CharField(choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
    ), max_length = 30)

    Teacher_Date_of_birth = models.DateField()

    

    Teacher_Social_Category = models.CharField(choices = (
        ('OPEN', 'OPEN'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('ORC', 'ORC'),
        ('OTHERS', 'OTHERS'),
    ), max_length = 30)

    Teacher_Type = models.CharField(choices =(
        ('Head Teacher', 'Head Teacher'),
        ('Acting Head Teacher', 'Acting Head Teacher'),
        ('Teacher', 'Teacher'),
        ('Instruction Positioned Teacher', 'Instruction Positioned Teacher'),
        ('Principal', 'Principal'),
        ('Vice-Principal', 'Vice-Principal'),
        ('Lecturer', 'Lecturer')
        
    ), max_length = 50)

    Teacher_Nature_Of_Appointment = models.CharField(choices = (
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('Part-Time', 'Part-Time')
    ), max_length = 30)

    Teacher_Date_of_Joining = models.DateField()
#9
    Teacher_Highest_Qualification_Academic = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post-Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_Highest_Qualification_Professional = models.CharField(choices = (
        ('Diploma or basic teacher training', 'Diploma or basic teacher training'),
        ('Bachelor of Elementary Education', 'Bachelor of Elementary Education'),
        ('B.Ed or equivalent', 'B.Ed or equivalent'),
        ('M.Ed or equivalent', 'M.Ed or equivalent'),
        ('Others', 'Others'),
        ('None', 'None'),
        ('Diploma or Degree in special Education', 'Diploma or Degree in special Education'),
        ('Pursuing a relevant course', 'Pursuing a relevant course')
    ), max_length = 100)


    Teacher_Classes_Taught = models.CharField(choices = (
        ('Primary Only', 'Primary Only'),
        ('Upper Primary Only', 'Upper Primary Only'),
        ('Primary and Upper Primary Only', 'Primary and Upper Primary Only'),
        ('Secondary Only', 'Secondary Only'),
        ('Higher Secondary Only', 'Higher Secondary Only'),
        ('Upper Primary and Secondary Only', 'Upper Primary and Secondary Only'),
        ('Secondary and Higher Secondary Only', 'Secondary and Higher Secondary Only'),
        ('Pre-Primary Only', 'Pre-Primary Only'),
        ('Pre-Primary and Primary Only', 'Pre-Primary and Primary Only')
    ), max_length = 100)

    Teacher_Appointment_Subject = models.CharField(choices = (
        ('All Subjects', 'All Subjects'),
        ('Language/Languages', 'Language/Languages'),
        ('Mathematics', 'Mathematics'),
        ('Environmental Studies', 'Environmental Studies '),
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Science', 'Science'),
        ('Social Study', 'Social Study '),
        ('Accountancy', 'Accountancy'),
        ('Biology', 'Biology'),
        ('Business Studies', 'Business Studies'),
        ('Chemistry', 'Chemistry'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
        ('Engineering Drawing', 'Engineering Drawing'),
        ('Fine Arts', 'Fine Arts'),
        ('Geography', 'Geography'),
        ('History', 'History'),
        ('Home Science', 'Home Science'),
        
        ('Philosophy', 'Philosophy'),
        ('Physics', 'Physics'),
        ('Political Science', 'Political Science'),
        ('Psychology', 'Psychology'),
        ('Foreign Language', 'Foreign Language'),
        ('Botany', 'Botany'),
        ('Zoology', 'Zoology'),
        ('Hindi', 'Hindi'),

        ('Sanskrit', 'Sanskrit'),
        ('Urdu', 'Urdu'),
        ('English', 'English'),
        ('Regional Language', 'Regional Language'),
        ('Art Education', 'Art Education'),
        ('Health and Physical Education', 'Health and Physical Education'),
        ('Work Education', 'Work Education'),
        ('Other Education', 'Other Education'),
    ), max_length = 50)
#13 
    Teacher_Main_Subject_1 = models.CharField(choices = (
        ('All Subjects', 'All Subjects'),
        ('Language/Languages', 'Language/Languages'),
        ('Mathematics', 'Mathematics'),
        ('Environmental Studies', 'Environmental Studies '),
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Science', 'Science'),
        ('Social Study', 'Social Study '),
        ('Accountancy', 'Accountancy'),
        ('Biology', 'Biology'),
        ('Business Studies', 'Business Studies'),
        ('Chemistry', 'Chemistry'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
        ('Engineering Drawing', 'Engineering Drawing'),
        ('Fine Arts', 'Fine Arts'),
        ('Geography', 'Geography'),
        ('History', 'History'),
        ('Home Science', 'Home Science'),
        
        ('Philosophy', 'Philosophy'),
        ('Physics', 'Physics'),
        ('Political Science', 'Political Science'),
        ('Psychology', 'Psychology'),
        ('Foreign Language', 'Foreign Language'),
        ('Botany', 'Botany'),
        ('Zoology', 'Zoology'),
        ('Hindi', 'Hindi'),

        ('Sanskrit', 'Sanskrit'),
        ('Urdu', 'Urdu'),
        ('English', 'English'),
        ('Regional Language', 'Regional Language'),
        ('Art Education', 'Art Education'),
        ('Health and Physical Education', 'Health and Physical Education'),
        ('Work Education', 'Work Education'),
        ('Other Education', 'Other Education'),
    ), max_length = 50)

    Teacher_Main_Subject_2 = models.CharField(choices = (
        ('All Subjects', 'All Subjects'),
        ('Language/Languages', 'Language/Languages'),
        ('Mathematics', 'Mathematics'),
        ('Environmental Studies', 'Environmental Studies '),
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Science', 'Science'),
        ('Social Study', 'Social Study '),
        ('Accountancy', 'Accountancy'),
        ('Biology', 'Biology'),
        ('Business Studies', 'Business Studies'),
        ('Chemistry', 'Chemistry'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
        ('Engineering Drawing', 'Engineering Drawing'),
        ('Fine Arts', 'Fine Arts'),
        ('Geography', 'Geography'),
        ('History', 'History'),
        ('Home Science', 'Home Science'),
        
        ('Philosophy', 'Philosophy'),
        ('Physics', 'Physics'),
        ('Political Science', 'Political Science'),
        ('Psychology', 'Psychology'),
        ('Foreign Language', 'Foreign Language'),
        ('Botany', 'Botany'),
        ('Zoology', 'Zoology'),
        ('Hindi', 'Hindi'),

        ('Sanskrit', 'Sanskrit'),
        ('Urdu', 'Urdu'),
        ('English', 'English'),
        ('Regional Language', 'Regional Language'),
        ('Art Education', 'Art Education'),
        ('Health and Physical Education', 'Health and Physical Education'),
        ('Work Education', 'Work Education'),
        ('Other Education', 'Other Education'),
    ), max_length = 50)

    ##################
    Teacher_BRC = models.IntegerField()

    Teacher_CRC = models.IntegerField()

    Teacher_DIET = models.IntegerField()

    ##################


    

    Teacher_Training_Received = models.CharField(choices = (
        ('Not Required', 'Not Required'),
        ('Subject Knowledge', 'Subject Knowledge'),
        ('Pedagogical Issues', 'Pedagogical Issues'),
        ('ICT skills ', 'ICT skills '),
        ('Knowledge and skills for CWSN', 'Knowledge and skills for CWSN'),
        ('Leadership and Management', 'Leadership and Management'),
        ('Sanitation and Hygeine', 'Sanitation and Hygeine'),
        ('Others', 'Others'),
    ), max_length=100)

    Teacher_Training_Need = models.CharField(choices = (
        ('Not Required', 'Not Required'),
        ('Subject Knowledge', 'Subject Knowledge'),
        ('Pedagogical Issues', 'Pedagogical Issues'),
        ('ICT skills ', 'ICT skills '),
        ('Knowledge and skills for CWSN', 'Knowledge and skills for CWSN'),
        ('Leadership and Management', 'Leadership and Management'),
        ('Sanitation and Hygeine', 'Sanitation and Hygeine'),
        ('Others', 'Others'),
    ), max_length=100)

    Teacher_Number_of_days_spent_on_non_teaching_assignment = models.IntegerField()

    Teacher_Math_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_Science_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_English_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_Language_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_Social_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 50)

    Teacher_Joining_Year = models.IntegerField()

    Teacher_Disability = models.CharField(choices = (
        ('Not Applicable', 'Not Applicable'),
        ('Loco motor', 'Loco motor'),
        ('Visuals', 'Visuals'),
        ('Other', 'Other'),
        ('Hearing Impaired', 'Hearing Impaired'),
    ), max_length=50)

    Teacher_Validity_for_CWSN = models.CharField(choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ), max_length = 50)

    Teacher_Trained_for_use_of_Computer = models.CharField(choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ), max_length = 50)

    Teacher_Marital_Status = models.CharField(choices = (
        ('Yes', "Yes"),
        ('No', "No")
    ), max_length=25, default = 'No')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    Teacher_Contact_Number = models.CharField(validators=[phone_regex], max_length=17)

    Teacher_Email = models.EmailField(max_length=254)

    def __str__(self):
        return self.Teacher_Name

    def get_absolute_url(self):
        return reverse("teach_staff:Teacher_Detail", kwargs={"pk": self.pk})
    
    Teacher_Other_Info = models.TextField(blank = True)