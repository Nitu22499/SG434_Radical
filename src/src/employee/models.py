from django.db import models

from profiles.models import School, User
from . import choices
from .validators import validate_phone_number


class Employee(models.Model):
    employee_user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_school = models.ForeignKey(School, on_delete=models.CASCADE)
    employee_social_category = models.CharField(choices=choices.SOCIAL_CATEGORY, max_length=30, default='OPEN',
                                                verbose_name='Social Category')
    employee_nature_of_appointment = models.CharField(choices=choices.NATURE_OF_APPOINTMENT, max_length=256, blank=True,
                                                      verbose_name='Nature of Appointment')
    employee_highest_academic_qualification = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256,
                                                               blank=True,
                                                               verbose_name='Highest Academic Qualification')
    employee_disability = models.CharField(choices=choices.DISABILITY, default='Not Applicable', max_length=256,
                                           verbose_name='Disability')
    employee_date_of_joining = models.DateField(verbose_name='Date of Joining')

    employee_is_married = models.BooleanField(default=False, max_length=25, verbose_name='Married?')
    employee_contact_number = models.BigIntegerField(validators=(validate_phone_number,), blank=True,
                                                  verbose_name='Contact Number')
    employee_email_address = models.EmailField(max_length=254, blank=True, verbose_name='Email Address')
    employee_other_info = models.TextField(blank=True, verbose_name='Other Information')

    def __str__(self):
        return self.employee_user.get_full_name()

    class Meta:
        ordering = ('employee_user__first_name', 'employee_user__last_name')


class Teacher(models.Model):
    teacher_employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    teacher_code = models.CharField(max_length=256, blank=True, null=True, verbose_name='Code')

    teacher_type = models.CharField(choices=choices.TEACHER_TYPE, max_length=256, blank=True,
                                    verbose_name='Type of Teacher')
    teacher_highest_professional_qualification = models.CharField(choices=choices.PROFESSIONAL_QUALIFICATION,
                                                                  max_length=256, default='None applicable',
                                                                  verbose_name='Highest Professional Qualification')
    teacher_classes_taught = models.CharField(choices=choices.CLASSES_TAUGHT, max_length=256, blank=True,
                                              verbose_name='Classes Taught')
    teacher_appointed_subject = models.CharField(choices=choices.SUBJECTS, max_length=256, blank=True,
                                                 verbose_name='Appointed Subject')
    teacher_main_subject_taught_1 = models.CharField(choices=choices.SUBJECTS, max_length=256, blank=True,
                                                     verbose_name='Main Subject Taught 1')
    Teacher_Main_Subject_2 = models.CharField(choices=choices.SUBJECTS, max_length=256, blank=True,
                                              verbose_name='Main Subject Taught 2')

    ##################
    """
    Total days of in-service training received in last academic year
    """
    teacher_brc = models.IntegerField(default=0, blank=True, verbose_name='Training received (BRC)',
                                      help_text='only for teachers in elementary')
    teacher_crc = models.IntegerField(default=0, blank=True, verbose_name='Training received (CRC)',
                                      help_text='only for teachers in elementary')
    teacher_diet = models.IntegerField(default=0, blank=True, verbose_name='Training received (DIET)',
                                       help_text='only for teachers in elementary')
    ##################

    teacher_training_received = models.CharField(choices=choices.TRAINING_OPTIONS, max_length=256, blank=True,
                                                 verbose_name='Training Received', default='Not Required')
    teacher_training_need = models.CharField(choices=choices.TRAINING_OPTIONS, max_length=256, blank=True,
                                             verbose_name='Training Need', default='Not Required')
    teacher_number_of_days_spent_on_non_teaching_assignment = models.IntegerField(
        default=0, blank=True,
        verbose_name='Number of days spent on non teaching assignments'
    )
    teacher_math_studied_up_to = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256, blank=True,
                                                  verbose_name='Maths studied up to')
    teacher_science_studied_up_to = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256, blank=True,
                                                     verbose_name='Science studied up to')
    teacher_english_studied_up_to = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256, blank=True,
                                                     verbose_name='English studied up to')
    teacher_language_studied_up_to = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256,
                                                      blank=True, verbose_name='Language studied up to')
    teacher_social_studies_studied_up_to = models.CharField(choices=choices.ACADEMIC_QUALIFICATION, max_length=256,
                                                            blank=True, verbose_name='Social Study studied up to')
    teacher_trained_for_teaching_cwsn = models.BooleanField(default=False, max_length=256, blank=True,
                                                            verbose_name='trained for CWSN')
    teacher_trained_for_use_of_computer = models.BooleanField(default=False, max_length=50, blank=True,
                                                              verbose_name='teach through computer')

    def __str__(self):
        return self.teacher_employee.employee_user.get_full_name()
