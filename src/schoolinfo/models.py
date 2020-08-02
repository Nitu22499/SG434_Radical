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

