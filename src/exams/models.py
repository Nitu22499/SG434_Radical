from django.db import models
from profiles.models import Subject, Student, class_choices, section_choices, stream_choices, School

from django.core.validators import MaxValueValidator, MinValueValidator

from misc.utilities import year_choices, academic_year

# Helper Class to have Min and Max Integer validation
class IntegerRangeField(models.IntegerField):

    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        if 'validators' in kwargs:
            validators = kwargs['validators']
        else:
            validators = []
        if min_value:
            validators.append(MinValueValidator(min_value))
        if max_value:
            validators.append(MaxValueValidator(max_value))
        kwargs['validators'] = validators
        super(IntegerRangeField, self).__init__(**kwargs)

    def formfield(self, **kwargs):
        context = {'min_value': self.min_value, 'max_value': self.max_value}
        context.update(kwargs)
        return super(IntegerRangeField, self).formfield(**context)


# choices for GRADE
# Marks Range | GRADE
# 91-100      | A1
# 81-90       | A2
# 71-80       | B1
# 61-70       | B2
# 51-60       | C1
# 41-50       | C2
# 33-40       | D
# 33 & below  | E(needs improvement)
grade_choices = (
    ('A1','A1'),
    ('A2', 'A2'),
    ('B1','B1'),
    ('B2','B2'),
    ('C1','C1'),
    ('C2','C2'),
    ('D','D'),
    ('E','E'),
    ('NA','NA')
)

# Grade Finder based on Total marks
def find_grade(total_marks):
    if total_marks > 90: return "A1"
    elif total_marks > 80: return "A2"
    elif total_marks > 70: return "B1"
    elif total_marks > 60: return "B2"
    elif total_marks > 50: return "C1"
    elif total_marks > 40: return "C2"
    elif total_marks > 32: return "D"
    else: return "E"

# Exam Model
class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    per_test_1 = IntegerRangeField(min_value=0, max_value=10, blank=True, null=True)
    notebook_1 = IntegerRangeField(min_value=0, max_value=5, blank=True, null=True)
    sea_1 = IntegerRangeField(min_value=0, max_value=5, blank=True, null=True)
    main_1 = IntegerRangeField(min_value=0, max_value=80, blank=True, null=True)
    grade_1 = models.CharField(max_length=10, default='NA', choices=grade_choices, editable=False)
    per_test_2 = IntegerRangeField(min_value=0, max_value=10, blank=True, null=True)
    notebook_2 = IntegerRangeField(min_value=0, max_value=5, blank=True, null=True)
    sea_2 = IntegerRangeField(min_value=0, max_value=5, blank=True, null=True)
    main_2 = IntegerRangeField(min_value=0, max_value=80, blank=True, null=True)
    grade_2 = models.CharField(max_length=10, default='NA', choices=grade_choices, editable=False)
    exam_year = models.CharField(max_length=50, default=academic_year(), choices=year_choices())
    exam_class = models.CharField(max_length=5, choices=class_choices, blank=True)
    exam_section = models.CharField(max_length=5, choices=section_choices, default = 'NA', blank=True)
    exam_stream = models.CharField(max_length=25, choices=stream_choices, default = 'NA', blank=True)
    exam_rollno = models.CharField(max_length=10, null=True, blank=True)

    @property
    def total_1(self):
        # returns Term-1 total marks obtained from 100
        try:
            return self.per_test_1 + self.notebook_1 + self.sea_1 + self.main_1
        except:
            return ''

    @property
    def total_2(self):
        # returns Term-2 total marks obtained from 100
        try:
            return self.per_test_2 + self.notebook_2 + self.sea_2 + self.main_2
        except:
            return ''

    def save(self, *args, **kwargs):
        try:
            self.grade_1 = find_grade(self.total_1)
            self.grade_2 = find_grade(self.total_2)
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student.user.first_name + " ("+ self.exam_class + "-" + self.exam_section + "-" + self.exam_rollno + ") " + self.subject.subject_name

# 3-point Grading Scheme
exam_cs_grade_choices = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('NA','NA')
)

class ExamCoScholastic(models.Model):
    exam_cs_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_cs_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_cs_grade_1 = models.CharField(max_length=5, default='NA', choices=exam_cs_grade_choices)
    exam_cs_grade_2 = models.CharField(max_length=5, default='NA', choices=exam_cs_grade_choices)
    exam_cs_year = models.CharField(max_length=50, default=academic_year(), choices=year_choices())
    exam_cs_class = models.CharField(max_length=5, choices=class_choices, blank=True)
    exam_cs_section = models.CharField(max_length=5, choices=section_choices, default = 'NA', blank=True)
    exam_cs_stream = models.CharField(max_length=25, choices=stream_choices, default = 'NA', blank=True)
    exam_cs_rollno = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.exam_cs_student.user.first_name + " ("+ self.exam_cs_class + "-" + self.exam_cs_section + "-" + self.exam_cs_rollno + ") " + self.exam_cs_subject.subject_name