from django.db import models
from profiles.models import School

class TimeStampMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    academic_year = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True

class EnrolmentPrePrimary(TimeStampMixin):
    epp_lkg_b = models.IntegerField(blank=True, null=True, verbose_name="Enrolment of boys in LKG")
    epp_lkg_g = models.IntegerField(blank=True, null=True, verbose_name="Enrolment of girls in LKG")
    epp_ukg_b = models.IntegerField(blank=True, null=True, verbose_name="Enrolment of boys in UKG")
    epp_ukg_g = models.IntegerField(blank=True, null=True, verbose_name="Enrolment of girls in UKG")
    epp_school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return "Boys in LKG and UKG are "+str(self.epp_lkg_b)+" and "+str(self.epp_ukg_b)+" resp.,Girls in LKG and UKG are "+str(self.epp_lkg_g)+" and "+str(self.epp_ukg_g)+" resp. ("+str(self.academic_year)+")"

class NewAdmissionsInGradeI(TimeStampMixin):
    nag_school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)

    # Boys
    nag_below_5_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of below 5 years age boys")
    nag_5_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 5 years age boys")
    nag_6_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 6 years age boys")
    nag_7_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 7 years age boys")
    nag_above_7_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of above 7 years age boys")
    # nag_total_b = models.IntegerField(blank=True, null=True, verbose_name="Admissions of above 7 years age boys")
    nag_same_school_b = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of boys with pre-school experience in same school")
    nag_another_school_b = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of boys with pre-school experience in another school")
    nag_anganwadi_school_b = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of boys with pre-school experience in Anganwadi/ECCE centre school")


    # Girls
    nag_below_5_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of below 5 years age girls")
    nag_5_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 5 years age girls")
    nag_6_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 6 years age girls")
    nag_7_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of 7 years age girls")
    nag_above_7_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of above 7 years age girls")
    # nag_total_g = models.IntegerField(blank=True, null=True, verbose_name="Admissions of above 7 years age girls")
    nag_same_school_g = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of girls with pre-school experience in same school")
    nag_another_school_g = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of girls with pre-school experience in another school")
    nag_anganwadi_school_g = models.IntegerField(blank=True, null=True, verbose_name="Out of the Total in Grade I Number of girls with pre-school experience in Anganwadi/ECCE centre school")

    @property
    def nag_total_b(self):
        try:
            return self.nag_below_5_b + self.nag_5_b + self.nag_6_b + self.nag_7_b + self.nag_above_7_b
        except:
            return ''
    
    @property
    def nag_total_g(self):
        try:
            return self.nag_below_5_g + self.nag_5_g + self.nag_6_g + self.nag_7_g + self.nag_above_7_g
        except:
            return ''

class_choices = (
    ('General', 'General'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC', 'OBC')
)
class EnrolmentBySocialCategory(TimeStampMixin):
    esc_school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=20, choices=class_choices, blank=True, null=True, verbose_name="Social Category Class Name")
    class_pre_primary_B = models.IntegerField(blank=True, null=True)
    class_pre_primary_G = models.IntegerField(blank=True, null=True)
    class_I_B = models.IntegerField(blank=True, null=True)
    class_I_G = models.IntegerField(blank=True, null=True)
    class_II_B = models.IntegerField(blank=True, null=True)
    class_II_G = models.IntegerField(blank=True, null=True)
    class_III_B = models.IntegerField(blank=True, null=True)
    class_III_G = models.IntegerField(blank=True, null=True)
    class_IV_B = models.IntegerField(blank=True, null=True)
    class_IV_G = models.IntegerField(blank=True, null=True)
    class_V_B = models.IntegerField(blank=True, null=True)
    class_V_G = models.IntegerField(blank=True, null=True)
    class_VI_B = models.IntegerField(blank=True, null=True)
    class_VI_G = models.IntegerField(blank=True, null=True)
    class_VII_B = models.IntegerField(blank=True, null=True)
    class_VII_G = models.IntegerField(blank=True, null=True)
    class_VIII_B = models.IntegerField(blank=True, null=True)
    class_VIII_G = models.IntegerField(blank=True, null=True)
    class_IX_B = models.IntegerField(blank=True, null=True)
    class_IX_G = models.IntegerField(blank=True, null=True)
    class_X_B = models.IntegerField(blank=True, null=True)
    class_X_G = models.IntegerField(blank=True, null=True)
    class_XI_B = models.IntegerField(blank=True, null=True)
    class_XI_G = models.IntegerField(blank=True, null=True)
    class_XII_B = models.IntegerField(blank=True, null=True)
    class_XII_G = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.academic_year + " (" + self.class_name + ")"

age_class_choices = (
    ('<5', 'below 5'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('>22', 'above 22')
)
class EnrolmentByAge(TimeStampMixin):
    eba_school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=20, choices=age_class_choices, blank=True, null=True, verbose_name="Age Class Name")
    class_I_B = models.IntegerField(blank=True, null=True)
    class_I_G = models.IntegerField(blank=True, null=True)
    class_II_B = models.IntegerField(blank=True, null=True)
    class_II_G = models.IntegerField(blank=True, null=True)
    class_III_B = models.IntegerField(blank=True, null=True)
    class_III_G = models.IntegerField(blank=True, null=True)
    class_IV_B = models.IntegerField(blank=True, null=True)
    class_IV_G = models.IntegerField(blank=True, null=True)
    class_V_B = models.IntegerField(blank=True, null=True)
    class_V_G = models.IntegerField(blank=True, null=True)
    class_VI_B = models.IntegerField(blank=True, null=True)
    class_VI_G = models.IntegerField(blank=True, null=True)
    class_VII_B = models.IntegerField(blank=True, null=True)
    class_VII_G = models.IntegerField(blank=True, null=True)
    class_VIII_B = models.IntegerField(blank=True, null=True)
    class_VIII_G = models.IntegerField(blank=True, null=True)
    class_IX_B = models.IntegerField(blank=True, null=True)
    class_IX_G = models.IntegerField(blank=True, null=True)
    class_X_B = models.IntegerField(blank=True, null=True)
    class_X_G = models.IntegerField(blank=True, null=True)
    class_XI_B = models.IntegerField(blank=True, null=True)
    class_XI_G = models.IntegerField(blank=True, null=True)
    class_XII_B = models.IntegerField(blank=True, null=True)
    class_XII_G = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.academic_year + " (" + self.class_name + ")"