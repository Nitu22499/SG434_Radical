from django.db import models
from profiles.models import School


class TimeStampMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    academic_year = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True

yn=(
        ('Yes',('Yes')),('No',('No'))
        )


class SchoolToilet(TimeStampMixin):
    st_school_name=models.OneToOneField(School, on_delete=models.CASCADE)
    st_boys_total_cwsn=models.CharField(max_length=10,blank=True)
    st_boys_func_cwsn=models.CharField(max_length=10,blank=True)
    st_girls_total_cwsn=models.CharField(max_length=10,blank=True)
    st_girls_func_cwsn=models.CharField(max_length=10,blank=True)
    st_total_cwsn=models.CharField(max_length=10,blank=True)
    st_func_cwsn=models.CharField(max_length=10,blank=True)
    st_boys_total_seats=models.CharField(max_length=10,blank=True)
    st_boys_func_seats=models.CharField(max_length=10,blank=True)
    st_girls_total_seats=models.CharField(max_length=10,blank=True)
    st_girls_func_seats=models.CharField(max_length=10,blank=True)
    st_total_seats=models.CharField(max_length=10,blank=True)
    st_func_seats=models.CharField(max_length=10,blank=True)
    st_boys_total_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_boys_func_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_girls_total_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_girls_func_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_total_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_func_cwsn_seats=models.CharField(max_length=10,blank=True)
    st_boys_total_urinals=models.CharField(max_length=10,blank=True)
    st_boys_func_urinals=models.CharField(max_length=10,blank=True)
    st_girls_total_urinals=models.CharField(max_length=10,blank=True)
    st_girls_func_urinals=models.CharField(max_length=10,blank=True)
    st_total_urinals=models.CharField(max_length=10,blank=True)
    st_func_urinals=models.CharField(max_length=10,blank=True)            




    def __str__(self):
        return str(self.st_school_name)

class SchoolItems(TimeStampMixin):
    sit_school_name = models.OneToOneField(School, on_delete=models.CASCADE)
    sit_lap_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_lap_units=models.CharField(max_length=10,blank=True)
    sit_lap_func=models.CharField(max_length=10,blank=True)
    sit_tab_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_tab_units=models.CharField(max_length=10,blank=True)
    sit_tab_func=models.CharField(max_length=10,blank=True)
    sit_desk_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_desk_units=models.CharField(max_length=10,blank=True)
    sit_desk_func=models.CharField(max_length=10,blank=True)
    sit_pc_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_pc_units=models.CharField(max_length=10,blank=True)
    sit_pc_func=models.CharField(max_length=10,blank=True)
    sit_boards_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_boards_units=models.CharField(max_length=10,blank=True)
    sit_boards_func=models.CharField(max_length=10,blank=True)
    sit_server_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_server_units=models.CharField(max_length=10,blank=True)
    sit_server_func=models.CharField(max_length=10,blank=True)
    sit_proj_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_proj_units=models.CharField(max_length=10,blank=True)
    sit_proj_func=models.CharField(max_length=10,blank=True)
    sit_lcd_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_lcd_units=models.CharField(max_length=10,blank=True)
    sit_lcd_func=models.CharField(max_length=10,blank=True)
    sit_print_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_print_units=models.CharField(max_length=10,blank=True)
    sit_print_func=models.CharField(max_length=10,blank=True)
    sit_scan_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_scan_units=models.CharField(max_length=10,blank=True)
    sit_scan_func=models.CharField(max_length=10,blank=True)
    sit_web_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_web_units=models.CharField(max_length=10,blank=True)
    sit_web_func=models.CharField(max_length=10,blank=True)
    sit_gen_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sit_gen_units=models.CharField(max_length=10,blank=True)
    sit_gen_func=models.CharField(max_length=10,blank=True)
    sit_net_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)

    sit_dth_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)

    sit_digital_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)

    sit_cwsn_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)


    def __str__(self):
        return str(self.sit_school_name)

class SchoolLibrary(TimeStampMixin):
    sli_school_name = models.OneToOneField(School, on_delete=models.CASCADE)
    sli_lib_avai=models.CharField(max_length=10,blank=True, choices=yn,null=True)
    sli_lib_books=models.CharField(max_length=10,blank=True,null=True)
    sli_lib_ncert=models.CharField(max_length=10,blank=True,null=True)
    sli_book_avai=models.CharField(max_length=10,blank=True,choices=yn,null=True)
    sli_book_books=models.CharField(max_length=10,blank=True,null=True)
    sli_book_ncert=models.CharField(max_length=10,blank=True,null=True)
    sli_reading_avai=models.CharField(max_length=10,blank=True,choices=yn,null=True)
    sli_reading_books=models.CharField(max_length=10,blank=True,null=True)
    sli_reading_ncert=models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return str(self.sli_school_name)


class SchoolReceipt(TimeStampMixin):
    sre_school_name= models.ForeignKey(School, on_delete=models.CASCADE)
    sre_re_composite=models.CharField(max_length=10,blank=True)
    sre_ex_composite=models.CharField(max_length=10,blank=True)
    sre_re_lib=models.CharField(max_length=10,blank=True)
    sre_ex_lib=models.CharField(max_length=10,blank=True)
    sre_re_sports=models.CharField(max_length=10,blank=True)
    sre_ex_sports=models.CharField(max_length=10,blank=True)
    sre_re_media=models.CharField(max_length=10,blank=True)
    sre_ex_media=models.CharField(max_length=10,blank=True)
    sre_re_smc=models.CharField(max_length=10,blank=True)
    sre_ex_smc=models.CharField(max_length=10,blank=True)
    sre_re_pre=models.CharField(max_length=10,blank=True)
    sre_ex_pre=models.CharField(max_length=10,blank=True)
    sre_re_repair=models.CharField(max_length=10,blank=True)
    sre_ex_repair=models.CharField(max_length=10,blank=True)
    sre_yes_non=models.CharField(max_length=10,blank=True,choices=yn)
    sre_non_name=models.CharField(max_length=10,blank=True)
    sre_non_amount=models.CharField(max_length=10,blank=True)
    sre_yes_psu=models.CharField(max_length=10,blank=True,choices=yn)
    sre_psu_name=models.CharField(max_length=10,blank=True)
    sre_psu_amount=models.CharField(max_length=10,blank=True)
    sre_yes_community=models.CharField(max_length=10,blank=True,choices=yn)
    sre_community_name=models.CharField(max_length=10,blank=True)
    sre_community_amount=models.CharField(max_length=10,blank=True)
    sre_other_yes=models.CharField(max_length=10,blank=True,choices=yn)
    sre_other_name=models.CharField(max_length=10,blank=True)
    sre_other_amount=models.CharField(max_length=10,blank=True)



    def __str__(self):
        return str(self.sre_school_name)

annual=(('Number of Students Appeared','Number of Students Appeared'),
('Number of Students Passed/Qualified','Number of Students Passed/Qualified'),
('Number of Students Passed with Marks>=60%','Number of Students Passed with Marks>=60%'))

class SchoolAnnual(TimeStampMixin):
    sa_school_name= models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=500, choices=annual,verbose_name="Name")
    sa_boys_gen=models.IntegerField(blank=True, null=True)
    sa_girls_gen=models.IntegerField(blank=True, null=True)
    sa_boys_sc=models.IntegerField(blank=True, null=True)
    sa_girls_sc=models.IntegerField(blank=True, null=True)
    sa_girls_sc=models.IntegerField(blank=True, null=True)
    sa_boys_st=models.IntegerField(blank=True, null=True)
    sa_girls_st=models.IntegerField(blank=True, null=True)
    sa_boys_obc=models.IntegerField(blank=True, null=True)
    sa_girls_obc=models.IntegerField(blank=True, null=True)
    sa_boys_total=models.IntegerField(blank=True, null=True)
    sa_girls_total=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.sa_school_name)

incentives_choice=(('Free textbooks','Free textbooks'),
('Uniforms','Uniforms'),('Transport facility','Transport facility'),
('Escort','Escort'),
('Bicycle','Bicycle'))

class SchoolIncentives(TimeStampMixin):
    si_school_name= models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=500, choices=incentives_choice, blank=True, null=True,verbose_name="Name")
    si_boys_gen=models.IntegerField(blank=True, null=True)
    si_girls_gen=models.IntegerField(blank=True, null=True)
    si_boys_sc=models.IntegerField(blank=True, null=True)
    si_girls_sc=models.IntegerField(blank=True, null=True)
    si_girls_sc=models.IntegerField(blank=True, null=True)
    si_boys_st=models.IntegerField(blank=True, null=True)
    si_girls_st=models.IntegerField(blank=True, null=True)
    si_boys_obc=models.IntegerField(blank=True, null=True)
    si_girls_obc=models.IntegerField(blank=True, null=True)
    si_boys_total=models.IntegerField(blank=True, null=True)
    si_girls_total=models.IntegerField(blank=True, null=True)
    si_boys_muslim=models.IntegerField(blank=True, null=True)
    si_girls_muslim=models.IntegerField(blank=True, null=True)
    si_boys_other=models.IntegerField(blank=True, null=True)
    si_girls_other=models.IntegerField(blank=True, null=True)


    def __str__(self):
        return str(self.si_school_name)

class SchoolSafety(TimeStampMixin):
    sst_school_name= models.OneToOneField(School, on_delete=models.CASCADE)
    sst_sdmp=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether the School Disaster Management Plan (SDMP) has been developed ?")
    sst_audit=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether Structural Safety Audit has been conducted ?")
    sst_non_audit=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether Non- structural Safety Audit has been conducted ?")
    sst_cctv=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether CCTV Cameras available in school ?")
    sst_fire=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether Fire Extinguishers are installed ? ")
    sst_nodal=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Does the school have a nodal teacher for school safety?")
    sst_teach_train=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether students and teachers undergo regular training in school safety and disaster preparedness ?")
    sst_disaster=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether disaster management is being taught as part of the curriculum ?")
    sst_self=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether school has received grant for Self Defense Training for Girls ?")
    sst_actual=models.CharField(max_length=10,blank=True,verbose_name="If yes, No. of students provided training (provide actual number of student trained)")
    sst_guidelines=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether the school has displayed safety guidelines on Display Board?")
    sst_first=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="Whether all teachers have received grant for working as first level counselors? (Only for Government Schools)")
    sst_counselling=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="i) Guidance & Counselling")
    sst_sensitization=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="ii) Sensitization of parents")
    sst_aware=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="iii) Awareness generation for Students and community")
    sst_provision=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="iv) Provision for taking feedback of the students")
    sst_suggestions=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="v) Suggestions/Complaint box in the schools")
    sst_copies=models.CharField(max_length=10,blank=True, choices=yn,verbose_name="vi) Providing copies of safety guidelines to the students")


    def __str__(self):
        return str(self.sst_school_name)



srte_choices=(
        ('I. In Private unaided and Specified Category schools under section 12(1)(c)','I. In Private unaided and Specified Category schools under section 12(1)(c) '),
        ('II. In Schools that have received land, building, equipment or other facilities at concessional rate','II. In Schools that have received land, building, equipment or other facilities at concessional rate')
    )
class SchoolRTE(TimeStampMixin):
    srte_school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=500, choices=srte_choices, blank=True, null=True,verbose_name="Name")
    srte_class_pre_B =models.IntegerField(blank=True, null=True)
    srte_class_pre_G = models.IntegerField(blank=True, null=True)
    srte_class_I_B = models.IntegerField(blank=True, null=True)
    srte_class_I_G = models.IntegerField(blank=True, null=True)
    srte_class_II_B = models.IntegerField(blank=True, null=True)
    srte_class_II_G = models.IntegerField(blank=True, null=True)
    srte_class_III_B = models.IntegerField(blank=True, null=True)
    srte_class_III_G = models.IntegerField(blank=True, null=True)
    srte_class_IV_B = models.IntegerField(blank=True, null=True)
    srte_class_IV_G = models.IntegerField(blank=True, null=True)
    srte_class_V_B = models.IntegerField(blank=True, null=True)
    srte_class_V_G = models.IntegerField(blank=True, null=True)
    srte_class_VI_B = models.IntegerField(blank=True, null=True)
    srte_class_VI_G = models.IntegerField(blank=True, null=True)
    srte_class_VII_B = models.IntegerField(blank=True, null=True)
    srte_class_VII_G = models.IntegerField(blank=True, null=True)
    srte_class_VIII_B = models.IntegerField(blank=True, null=True)
    srte_class_VIII_G = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.academic_year + " (" + self.class_name + ")" 

class SchoolEWS(TimeStampMixin):
    sews_school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=500, blank=True, null=True,verbose_name="In Schools that have received land, building, equipment or other facilities at concessional rate")
    sews_class_IX_B =models.IntegerField(blank=True, null=True)
    sews_class_IX_G = models.IntegerField(blank=True, null=True)
    sews_class_X_B = models.IntegerField(blank=True, null=True)
    sews_class_X_G = models.IntegerField(blank=True, null=True)
    sews_class_XI_B = models.IntegerField(blank=True, null=True)
    sews_class_XI_G = models.IntegerField(blank=True, null=True)
    sews_class_XII_B = models.IntegerField(blank=True, null=True)
    sews_class_XII_G = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.academic_year + " (" + self.class_name + ")" 

