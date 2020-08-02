from django.db import models

class Teaching_Staff_NonTeachers_Info(models.Model):
    NonTeachers_School = models.ForeignKey(School, on_delete = models.CASCADE)
    NonTeachers_Name = models.CharField(max_length = 25, verbose_name='Name')

    NonTeachers_Gender = models.CharField(choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
    ), max_length = 30, blank = True, verbose_name= 'Gender')

    NonTeachers_Date_of_birth = models.DateField(null=True, blank = True,verbose_name= 'Date of Birth')

    NonTeachers_Social_Category = models.CharField(choices = (
        ('OPEN', 'OPEN'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('ORC', 'ORC'),
        ('OTHERS', 'OTHERS'),
    ), max_length = 30, blank = True,verbose_name= 'Social Category')

    NonTeachers_Nature_Of_Appointment = models.CharField(choices = (
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('Part-Time', 'Part-Time')
    ), max_length = 30, blank = True,verbose_name= 'Nature of Appointment')

    NonTeachers_Date_of_Joining = models.DateField(blank = True, null = True,verbose_name= 'Date of Joining')
    NonTeachers_Joining_Year = models.IntegerField(blank = True, null = True,verbose_name= 'Joining Year')

    NonTeachers_Disability = models.CharField(choices = (
        ('Not Applicable', 'Not Applicable'),
        ('Loco motor', 'Loco motor'),
        ('Visuals', 'Visuals'),
        ('Other', 'Other'),
        ('Hearing Impaired', 'Hearing Impaired'),
    ), max_length=50, blank = True,verbose_name= 'Disability')

    NonTeacher_Qualifications = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate')
        
    ), max_length = 50, blank = True,verbose_name= 'Qualification')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    NonTeachers_Contact_Number = models.CharField(validators=[phone_regex], max_length=30, blank = True,verbose_name= 'Contact Number')

    NonTeachers_Email = models.EmailField(max_length=254, blank = True,verbose_name= 'Email')

    def __str__(self):
        return self.NonTeachers_Name

    def get_absolute_url(self):
        return reverse("teach_staff:NonTeachers_Detail", kwargs={"pk": self.pk})
    
    NonTeachers_Other_Info = models.TextField(blank = True,verbose_name= 'Other Info')




class Teaching_Staff_Info(models.Model):
    Teacher_School = models.ForeignKey(School, on_delete = models.CASCADE)

    Teacher_Code = models.CharField(max_length = 256, blank = True,null = True,verbose_name= 'Code')
    Teacher_Name = models.CharField(max_length = 256, blank = True,verbose_name= 'Name')

    Teacher_Gender = models.CharField(choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
    ), max_length = 30, blank = True,verbose_name= 'Gender')

    Teacher_Date_of_birth = models.DateField(blank = True,verbose_name= 'Date of Birth', null = True)

    

    Teacher_Social_Category = models.CharField(choices = (
        ('OPEN', 'OPEN'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('ORC', 'ORC'),
        ('OTHERS', 'OTHERS'),
    ), max_length = 30, blank = True,verbose_name= 'Social Category')

    Teacher_Type = models.CharField(choices =(
        ('Head Teacher', 'Head Teacher'),
        ('Acting Head Teacher', 'Acting Head Teacher'),
        ('Teacher', 'Teacher'),
        ('Instruction Positioned Teacher', 'Instruction Positioned Teacher'),
        ('Principal', 'Principal'),
        ('Vice-Principal', 'Vice-Principal'),
        ('Lecturer', 'Lecturer')
        
    ), max_length = 256, blank = True,verbose_name= 'Type')

    Teacher_Nature_Of_Appointment = models.CharField(choices = (
        ('Regular', 'Regular'),
        ('Contract', 'Contract'),
        ('Part-Time', 'Part-Time')
    ), max_length = 256, blank = True,verbose_name= 'Nature of Appointment')

    Teacher_Date_of_Joining = models.DateField(blank = True, null = True,verbose_name= 'Date of Joining')
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
    ), max_length = 256, blank = True,verbose_name= 'Highest Academic Qualification')

    Teacher_Highest_Qualification_Professional = models.CharField(choices = (
        ('Diploma or basic teacher training', 'Diploma or basic teacher training'),
        ('Bachelor of Elementary Education', 'Bachelor of Elementary Education'),
        ('B.Ed or equivalent', 'B.Ed or equivalent'),
        ('M.Ed or equivalent', 'M.Ed or equivalent'),
        ('Others', 'Others'),
        ('None', 'None'),
        ('Diploma or Degree in special Education', 'Diploma or Degree in special Education'),
        ('Pursuing a relevant course', 'Pursuing a relevant course')
    ), max_length = 256, blank = True,verbose_name= 'Highest Professional Qualification')


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
    ), max_length = 256, blank = True,verbose_name= 'Classes Taught')

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
    ), max_length = 256, blank = True, verbose_name= 'Allocated Subject')
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
    ), max_length = 256, blank = True, verbose_name= 'Main Subject 1')

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
    ), max_length = 256, blank = True, verbose_name= 'Main Subject 2')

    ##################
    Teacher_BRC = models.IntegerField(null = True, blank = True, verbose_name= 'BRC')

    Teacher_CRC = models.IntegerField(null = True, blank = True, verbose_name= 'CRC')

    Teacher_DIET = models.IntegerField(null = True, blank = True, verbose_name= 'DIET')

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
    ), max_length=256, blank = True, verbose_name= 'Training Received')

    Teacher_Training_Need = models.CharField(choices = (
        ('Not Required', 'Not Required'),
        ('Subject Knowledge', 'Subject Knowledge'),
        ('Pedagogical Issues', 'Pedagogical Issues'),
        ('ICT skills ', 'ICT skills '),
        ('Knowledge and skills for CWSN', 'Knowledge and skills for CWSN'),
        ('Leadership and Management', 'Leadership and Management'),
        ('Sanitation and Hygeine', 'Sanitation and Hygeine'),
        ('Others', 'Others'),
    ), max_length=256, blank = True, verbose_name= 'Training Required')

    Teacher_Number_of_days_spent_on_non_teaching_assignment = models.IntegerField(null = True, blank = True, verbose_name= 'Number of days spent on non teaching assignments')

    Teacher_Math_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 256, blank = True, verbose_name= 'Maths Knowledge')

    Teacher_Science_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 256, blank = True, verbose_name= 'Science Knowledge')

    Teacher_English_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 256, blank = True, verbose_name= 'English Knowledge')

    Teacher_Language_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 256, blank = True, verbose_name= 'Language Knowledge')

    Teacher_Social_Study_Knowledge = models.CharField(choices = (
        ('Below Secondary', 'Below Secondary'),
        ('Secondary', 'Secondary'),
        ('High Secondary', 'High Secondary'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('M Phil', 'M Phil'),
        ('Ph.D', 'Ph.D'),
        ('Post-Doctoral', 'Post-Doctoral')
    ), max_length = 256, blank = True, verbose_name= 'Social Study Knowledge')

    Teacher_Joining_Year = models.IntegerField(verbose_name= 'Joining Year', blank = True, null = True)

    Teacher_Disability = models.CharField(choices = (
        ('Not Applicable', 'Not Applicable'),
        ('Loco motor', 'Loco motor'),
        ('Visuals', 'Visuals'),
        ('Other', 'Other'),
        ('Hearing Impaired', 'Hearing Impaired'),
    ), max_length=256, blank = True, verbose_name= 'Disability')

    Teacher_Validity_for_CWSN = models.CharField(choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ), max_length = 256, blank = True, verbose_name= 'Validity for CWSN')

    Teacher_Trained_for_use_of_Computer = models.CharField(choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    ), max_length = 50, blank = True, verbose_name= 'Computer Training')

    Teacher_Marital_Status = models.CharField(choices = (
        ('Yes', "Yes"),
        ('No', "No")
    ), max_length=25, default = 'No', verbose_name= 'Marital Status')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    Teacher_Contact_Number = models.CharField(validators=[phone_regex], max_length=50, blank = True, verbose_name= 'Phone Regex')

    Teacher_Email = models.EmailField(max_length=254, blank = True, verbose_name= 'Email')

    def __str__(self):
        return self.Teacher_Name

    def get_absolute_url(self):
        return reverse("teach_staff:Teacher_Detail", kwargs={"pk": self.pk})
    
    Teacher_Other_Info = models.TextField(blank = True, verbose_name= 'Other Information')
