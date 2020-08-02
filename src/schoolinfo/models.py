from django.db import models
from profiles.models import School

school_located_choices = (('Rural', 'Rural'), ('Urban', 'Urban'))

class TimeStampMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    academic_year = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True


class SchoolProfile(TimeStampMixin):
    sp_school = models.OneToOneField(School, on_delete=models.CASCADE)
    sp_school_name = models.CharField(max_length=250, verbose_name='School Name (In Capital Letters)')
    sp_school_located = models.CharField(max_length=50, choices=school_located_choices, blank=True, verbose_name='Is the school located in Rural or Urban Area')
    sp_village_ward = models.CharField(max_length=250, blank=True, verbose_name='(a) Village Name')

    def __str__(self):
        return self.sp_school_name

class_choices = (
    ('General', 'General'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC', 'OBC'),
    ('Muslim', 'Muslim'),
    ('Christian', 'Christian'),
    ('Sikh', 'Sikh'),
    ('Buddhist', 'Buddhist'),
    ('Parsi', 'Parsi'),
    ('Jain', 'Jain'),
    ('Other', 'Other')
)

class RepeatersByGrade(models.Model):
    academic_year = models.CharField(max_length=50, blank=True)
    is_minority_group = models.BooleanField(default=False)
    class_name = models.CharField(max_length=20, choices=class_choices, blank=True, null=True, verbose_name="Social Category Class Name")
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

    def save(self, *args, **kwargs):
        if self.class_name in ['Muslim','Christian','Sikh','Buddhist','Parsi','Jain','Other']:
            self.is_minority_group = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.academic_year + " (" + self.class_name + ")"


status_of_building=(('Private',('Private')),
            ('Rented',('Rented')),
            ('Government',('Government')),
            ('Government School in a rent free building',('Government School in a rent free building')),
            ('No Building',('No Building')),
            ('Building',('Building')),
            ('Under Construction',('Under Construction')),
            ('School running in other Department Building',('School running in other Department Building')))

type_boundary_wall=(('Pucca',('Pucca')),('Pucca but broken',('Pucca but broken')),('Barbed wire fencing',('Barbed wire fencing')),
('Hedges',('Hedges')),('boundary walls',('boundary walls')),('others',('others')),('Partial',('Partial')),('Under Construction',('Under Construction')))

ynp=(
        ('Yes',('Yes')),('No',('No')),('Yes, but not functional',('Yes, but not functional'))
        )

de_worming=(('Complete(two doses)',('Complete(two doses)')),('Partially(one dose)',('Partially(one dose)')),('Not given',('Not given')))

special_educator=(('Dedicated',('Dedicated')),('At cluster level',('At cluster level')),('No',('No')))

dustbins_class=(('Yes and all',('Yes and all')),('No',('No')),('Yes but some',('Yes but some')))

which_comp_lab=(('ICT',('ICT')),('CAL',('CAL')),('Both',('Both')),('None',('None')))

ict_model=(('BOOT Model',('BOOT Model')),('BOO Model',('BOO Model')),('Other',('Other')))

ict_instructor=(('Full time',('Full time')),('Part Time',('Part Time')),('Not Available',('Not Available')))

class PhysicalFacilities(TimeStampMixin):
    pf_school = models.OneToOneField(School, on_delete=models.CASCADE)
    pf_status=models.CharField(max_length=50,choices=status_of_building, blank=True,verbose_name='Status of the School building')
    
    #2.2

    pf_boundary_type=models.CharField(max_length=50,choices=type_boundary_wall, blank=True,verbose_name='Type of boundary wall')
    pf_classrooms_instructional=models.CharField(max_length=50, blank=True,verbose_name='(a1) No. of Classrooms used for instructional purposes')
    pf_classrooms_construction=models.CharField(max_length=50, blank=True,verbose_name='(a2) No. of Classrooms under construction')
    pf_dilapidated=models.CharField(max_length=50, blank=True,verbose_name='(a3) Total Classrooms in dilapidated condition')
    pf_classrooms_instructional_pre_pri=models.CharField(max_length=10,blank=True,verbose_name='Pre-primary')
    pf_classrooms_instructional_pri=models.CharField(max_length=10,blank=True,verbose_name='Primary')
    pf_classrooms_instructional_upper_pri=models.CharField(max_length=10,blank=True,verbose_name='Upper primary')
    pf_classrooms_instructional_sec=models.CharField(max_length=10,blank=True,verbose_name='Secondary')
    pf_classrooms_instructional_higher_sec=models.CharField(max_length=10,blank=True,verbose_name='Higher Secondary')
    pf_classrooms_available=models.CharField(max_length=10,blank=True,verbose_name='(b) Total number of rooms other than classrooms available in School:')

    #2.3(c)

    pf_land_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether land is available for expansion of school facilities')
    pf_separate_head_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether separate room for Head Teacher/Principle available')
    pf_schools_toilet=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Does the school have toilet?')

    #2.7(a)

    pf_water_available=models.CharField(max_length=10,blank=True,verbose_name='(a) How many have running water available in the toilet/urinal for flushing and cleaning?')
    pf_hand_soap_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(b) Is hand washing facility with soap available near toilets/urinals block?')
    pf_incinerator_girls=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(c) Whether incinerator is available in/attached to girls toilet?')
    
    pf_drinking_water_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether drinking water is available in the school premises?')

    #2.8(a)

    pf_purifier_available=models.CharField(max_length=25,choices=ynp,blank=True,verbose_name='Whether water purifier/RO is available in the school?')
    pf_water_testing=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether water quality is tested from water testing lab?')
    pf_rain_harvesting=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Does the school have provision for rain water harvesting')
    pf_hand_washing_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether hand washing facility with soap available')
    pf_rain_harvesting=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Does the school have provision for rain water harvesting?')
    pf_hand_washing_available=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether hand washing facility with soap available for available for washing hands before and after meal?')
    pf_number_hand_washing=models.CharField(max_length=10,blank=True,verbose_name='(a) Number of wash points')
    pf_electricity_connection=models.CharField(max_length=30,choices=ynp,blank=True,verbose_name='Whether electricity connection is available in the school ?')
    pf_solar_panel=models.CharField(max_length=30,choices=ynp,blank=True,verbose_name='Whether solar panel available in school?')

    #2.12(a)

    pf_librarian=models.CharField(max_length=10,choices=yn,blank=True,verbose_name=' Does the school have a full-time librarian?')
    pf_magazine=models.CharField(max_length=10,choices=yn,blank=True,verbose_name=' Does the School subsribe to newspapers/magazines?')

    pf_playground_facility=models.CharField(max_length=28,choices=yn,blank=True,verbose_name='Whether Playground facility is available?')
    pf_other_arrangement=models.CharField(max_length=28,choices=yn,blank=True,verbose_name='(a) if no, whether school has made adequate arrangements for children to play outdoor games and other physical activities in an adjoining playground/municipal park etc.')
    
    pf_medical_check_up=models.CharField(max_length=20,choices=yn,blank=True,verbose_name='Whether Medical check-up is conducted(last year)?')
    pf_total_medical_check_ups=models.CharField(max_length=10,blank=True,verbose_name='(a)Total Number of  Medical check-ups is conducted(last year)?')
    
    pf_de_worming_given=models.CharField(max_length=20,choices=de_worming,blank=True,verbose_name='(b)De-worming tablets given to children?')
    pf_iron_folic=models.CharField(max_length=20,choices=yn,blank=True,verbose_name='(c)Iron and Folic acid tablets given to children')

    pf_ramp_disabled=models.CharField(max_length=20,choices=yn,blank=True,verbose_name='Whether ramp for disabled children to access school building exists?')
    pf_hand_rails=models.CharField(max_length=20,choices=yn,blank=True,verbose_name='(a) If yes,whether Hand-rails for ramp is available?')
    
    pf_school_special_edu=models.CharField(max_length=20,choices=special_educator,blank=True,verbose_name='Whether School has special educator?')
    pf_kitchen_garden=models.CharField(max_length=20,choices=yn,blank=True,verbose_name='Whether Kitchen Garden is available in school?')

    
    pf_dustbins_class=models.CharField(max_length=41,choices=dustbins_class,blank=True,verbose_name='(a) Class room')
    pf_dustbins_toilet=models.CharField(max_length=41,choices=yn,blank=True,verbose_name='(b) Toilet')
    pf_dustbins_kitchen=models.CharField(max_length=41,choices=yn,blank=True,verbose_name='(c) kitchen')
    pf_students_furniture=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='No. of Students for whom furniture is available?')

    pf_sep_room_head_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(a) Separate Room for Assistant Head Teacher/Vice principal')
    pf_sep_girls_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(b) Separate common room for girls')
    pf_staff_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(c) Staffroom for teachers')
    pf_arts_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(d) Co-curricular activity room/arts and crafts room')
    pf_staff_quarters_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(e) Staff quarters(including residential quarters for Head Teacher/Principal and Asst. Head Teacher/Vice Principal)')
    pf_science_lab_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(f) Integrated Science laboratory(integrated laboratory is the one in which Physics,Chemistry and Biology practical are held)for Secondary sections only')
    pf_lib_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(g) Library room')
    pf_comp_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(h) Computer room')
    pf_tinkering_sec=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='(i) Tinkering Lab')

    #2.21

    pf_equip_audio=models.CharField(max_length=100,choices=ynp,blank=True,verbose_name='(a) Audio/Visual/Public Address System')
    pf_equip_sci_kit=models.CharField(max_length=100,choices=ynp,blank=True,verbose_name='(b) Science Kit')
    pf_equip_math_kit=models.CharField(max_length=100,choices=ynp,blank=True,verbose_name='(c) Math kit')
    pf_equip_biometric=models.CharField(max_length=100,choices=ynp,blank=True,verbose_name='(d) Biometric device')

    
    pf_which_comp_lab=models.CharField(max_length=100,choices=which_comp_lab,blank=True,verbose_name='Which Computer lab is available in the School?')
    pf_ict_year=models.CharField(max_length=100,blank=True,verbose_name='(a)Year of implementation')
    pf_ict_functional=models.CharField(max_length=100,choices=yn,blank=True,verbose_name='(b)Whether ICT lab is functional or not?')

    
    pf_ict_model=models.CharField(max_length=100,choices=ict_model,blank=True,verbose_name='(c)Which Model is implemented in the School?')
    
    
    pf_ict_instructor=models.CharField(max_length=100,choices=ict_instructor,blank=True,verbose_name='(d)Type of ICT instructor in the School?')

    #2.32

    pf_ict_for_teaching=models.CharField(max_length=10,choices=yn,blank=True,verbose_name='Whether ICT based tools are used for teaching?')
    pf_ict_for_teaching_hours=models.CharField(max_length=10,blank=True,verbose_name='(a) If yes, Number of Hours spent per week')

    def __str__(self):
        return str(self.pf_school)
