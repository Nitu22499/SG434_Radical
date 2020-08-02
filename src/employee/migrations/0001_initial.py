# Generated by Django 3.0.8 on 2020-08-01 10:29

from django.db import migrations, models
import django.db.models.deletion
import employee.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_social_category', models.CharField(choices=[('OPEN', 'OPEN'), ('SC', 'SC'), ('ST', 'ST'), ('OBC', 'OBC'), ('ORC', 'ORC'), ('OTHERS', 'OTHERS')], default='OPEN', max_length=30, verbose_name='Social Category')),
                ('employee_nature_of_appointment', models.CharField(blank=True, choices=[('Regular', 'Regular'), ('Contract', 'Contract'), ('Part-Time', 'Part-Time')], max_length=256, verbose_name='Nature of Appointment')),
                ('employee_highest_academic_qualification', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='Highest Academic Qualification')),
                ('employee_disability', models.CharField(choices=[('Not Applicable', 'Not Applicable'), ('Loco motor', 'Loco motor'), ('Visuals', 'Visuals'), ('Other', 'Other'), ('Hearing Impaired', 'Hearing Impaired')], default='Not Applicable', max_length=256, verbose_name='Disability')),
                ('employee_date_of_joining', models.DateField(verbose_name='Date of Joining')),
                ('employee_is_married', models.BooleanField(default=False, max_length=25, verbose_name='Married?')),
                ('employee_contact_number', models.BigIntegerField(blank=True, validators=[employee.validators.validate_phone_number], verbose_name='Contact Number')),
                ('employee_email_address', models.EmailField(blank=True, max_length=254, verbose_name='Email Address')),
                ('employee_other_info', models.TextField(blank=True, verbose_name='Other Information')),
            ],
            options={
                'ordering': ('employee_user__first_name', 'employee_user__last_name'),
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_code', models.CharField(blank=True, max_length=256, null=True, verbose_name='Code')),
                ('teacher_type', models.CharField(blank=True, choices=[('Head Teacher', 'Head Teacher'), ('Acting Head Teacher', 'Acting Head Teacher'), ('Teacher', 'Teacher'), ('Instruction Positioned Teacher', 'Instruction Positioned Teacher'), ('Principal', 'Principal'), ('Vice-Principal', 'Vice-Principal'), ('Lecturer', 'Lecturer')], max_length=256, verbose_name='Type of Teacher')),
                ('teacher_highest_professional_qualification', models.CharField(choices=[('Diploma or basic teacher training', 'Diploma or basic teacher training'), ('Bachelor of Elementary Education', 'Bachelor of Elementary Education'), ('B.Ed or equivalent', 'B.Ed or equivalent'), ('M.Ed or equivalent', 'M.Ed or equivalent'), ('Others', 'Others'), ('None applicable', 'None applicable'), ('Diploma or Degree in special Education', 'Diploma or Degree in special Education'), ('Pursuing a relevant course', 'Pursuing a relevant course')], default='None applicable', max_length=256, verbose_name='Highest Professional Qualification')),
                ('teacher_classes_taught', models.CharField(blank=True, choices=[('Primary Only', 'Primary Only'), ('Upper Primary Only', 'Upper Primary Only'), ('Primary and Upper Primary Only', 'Primary and Upper Primary Only'), ('Secondary Only', 'Secondary Only'), ('Higher Secondary Only', 'Higher Secondary Only'), ('Upper Primary and Secondary Only', 'Upper Primary and Secondary Only'), ('Secondary and Higher Secondary Only', 'Secondary and Higher Secondary Only'), ('Pre-Primary Only', 'Pre-Primary Only'), ('Pre-Primary and Primary Only', 'Pre-Primary and Primary Only')], max_length=256, verbose_name='Classes Taught')),
                ('teacher_appointed_subject', models.CharField(blank=True, choices=[('All Subjects', 'All Subjects'), ('Language/Languages', 'Language/Languages'), ('Mathematics', 'Mathematics'), ('Environmental Studies', 'Environmental Studies '), ('Sports', 'Sports'), ('Music', 'Music'), ('Science', 'Science'), ('Social Study', 'Social Study '), ('Accountancy', 'Accountancy'), ('Biology', 'Biology'), ('Business Studies', 'Business Studies'), ('Chemistry', 'Chemistry'), ('Computer Science', 'Computer Science'), ('Economics', 'Economics'), ('Engineering Drawing', 'Engineering Drawing'), ('Fine Arts', 'Fine Arts'), ('Geography', 'Geography'), ('History', 'History'), ('Home Science', 'Home Science'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Political Science', 'Political Science'), ('Psychology', 'Psychology'), ('Foreign Language', 'Foreign Language'), ('Botany', 'Botany'), ('Zoology', 'Zoology'), ('Hindi', 'Hindi'), ('Sanskrit', 'Sanskrit'), ('Urdu', 'Urdu'), ('English', 'English'), ('Regional Language', 'Regional Language'), ('Art Education', 'Art Education'), ('Health and Physical Education', 'Health and Physical Education'), ('Work Education', 'Work Education'), ('Other Education', 'Other Education')], max_length=256, verbose_name='Appointed Subject')),
                ('teacher_main_subject_taught_1', models.CharField(blank=True, choices=[('All Subjects', 'All Subjects'), ('Language/Languages', 'Language/Languages'), ('Mathematics', 'Mathematics'), ('Environmental Studies', 'Environmental Studies '), ('Sports', 'Sports'), ('Music', 'Music'), ('Science', 'Science'), ('Social Study', 'Social Study '), ('Accountancy', 'Accountancy'), ('Biology', 'Biology'), ('Business Studies', 'Business Studies'), ('Chemistry', 'Chemistry'), ('Computer Science', 'Computer Science'), ('Economics', 'Economics'), ('Engineering Drawing', 'Engineering Drawing'), ('Fine Arts', 'Fine Arts'), ('Geography', 'Geography'), ('History', 'History'), ('Home Science', 'Home Science'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Political Science', 'Political Science'), ('Psychology', 'Psychology'), ('Foreign Language', 'Foreign Language'), ('Botany', 'Botany'), ('Zoology', 'Zoology'), ('Hindi', 'Hindi'), ('Sanskrit', 'Sanskrit'), ('Urdu', 'Urdu'), ('English', 'English'), ('Regional Language', 'Regional Language'), ('Art Education', 'Art Education'), ('Health and Physical Education', 'Health and Physical Education'), ('Work Education', 'Work Education'), ('Other Education', 'Other Education')], max_length=256, verbose_name='Main Subject Taught 1')),
                ('Teacher_Main_Subject_2', models.CharField(blank=True, choices=[('All Subjects', 'All Subjects'), ('Language/Languages', 'Language/Languages'), ('Mathematics', 'Mathematics'), ('Environmental Studies', 'Environmental Studies '), ('Sports', 'Sports'), ('Music', 'Music'), ('Science', 'Science'), ('Social Study', 'Social Study '), ('Accountancy', 'Accountancy'), ('Biology', 'Biology'), ('Business Studies', 'Business Studies'), ('Chemistry', 'Chemistry'), ('Computer Science', 'Computer Science'), ('Economics', 'Economics'), ('Engineering Drawing', 'Engineering Drawing'), ('Fine Arts', 'Fine Arts'), ('Geography', 'Geography'), ('History', 'History'), ('Home Science', 'Home Science'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Political Science', 'Political Science'), ('Psychology', 'Psychology'), ('Foreign Language', 'Foreign Language'), ('Botany', 'Botany'), ('Zoology', 'Zoology'), ('Hindi', 'Hindi'), ('Sanskrit', 'Sanskrit'), ('Urdu', 'Urdu'), ('English', 'English'), ('Regional Language', 'Regional Language'), ('Art Education', 'Art Education'), ('Health and Physical Education', 'Health and Physical Education'), ('Work Education', 'Work Education'), ('Other Education', 'Other Education')], max_length=256, verbose_name='Main Subject Taught 2')),
                ('teacher_brc', models.IntegerField(blank=True, default=0, help_text='only for teachers in elementary', verbose_name='Training received (BRC)')),
                ('teacher_crc', models.IntegerField(blank=True, default=0, help_text='only for teachers in elementary', verbose_name='Training received (CRC)')),
                ('teacher_diet', models.IntegerField(blank=True, default=0, help_text='only for teachers in elementary', verbose_name='Training received (DIET)')),
                ('teacher_training_received', models.CharField(blank=True, choices=[('Not Required', 'Not Required'), ('Subject Knowledge', 'Subject Knowledge'), ('Pedagogical Issues', 'Pedagogical Issues'), ('ICT skills ', 'ICT skills '), ('Knowledge and skills for CWSN', 'Knowledge and skills for CWSN'), ('Leadership and Management', 'Leadership and Management'), ('Sanitation and Hygiene', 'Sanitation and Hygiene'), ('Others', 'Others')], default='Not Required', max_length=256, verbose_name='Training Received')),
                ('teacher_training_need', models.CharField(blank=True, choices=[('Not Required', 'Not Required'), ('Subject Knowledge', 'Subject Knowledge'), ('Pedagogical Issues', 'Pedagogical Issues'), ('ICT skills ', 'ICT skills '), ('Knowledge and skills for CWSN', 'Knowledge and skills for CWSN'), ('Leadership and Management', 'Leadership and Management'), ('Sanitation and Hygiene', 'Sanitation and Hygiene'), ('Others', 'Others')], default='Not Required', max_length=256, verbose_name='Training Need')),
                ('teacher_number_of_days_spent_on_non_teaching_assignment', models.IntegerField(blank=True, default=0, verbose_name='Number of days spent on non teaching assignments')),
                ('teacher_math_studied_up_to', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='Maths studied up to')),
                ('teacher_science_studied_up_to', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='Science studied up to')),
                ('teacher_english_studied_up_to', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='English studied up to')),
                ('teacher_language_studied_up_to', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='Language studied up to')),
                ('teacher_social_studies_studied_up_to', models.CharField(blank=True, choices=[('Below Secondary', 'Below Secondary'), ('Secondary', 'Secondary'), ('High Secondary', 'High Secondary'), ('Graduate', 'Graduate'), ('Post-Graduate', 'Post Graduate'), ('M Phil', 'M Phil'), ('Ph.D', 'Ph.D'), ('Post-Doctoral', 'Post-Doctoral')], max_length=256, verbose_name='Social Study studied up to')),
                ('teacher_trained_for_teaching_cwsn', models.BooleanField(blank=True, default=False, max_length=256, verbose_name='trained for CWSN')),
                ('teacher_trained_for_use_of_computer', models.BooleanField(blank=True, default=False, max_length=50, verbose_name='teach through computer')),
                ('teacher_employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
            ],
        ),
    ]
