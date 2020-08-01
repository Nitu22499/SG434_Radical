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

