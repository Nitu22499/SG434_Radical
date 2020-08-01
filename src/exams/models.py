from django.db import models
from profiles.models import Subject, Student


# Helper Class to have Min and Max Integer validation
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


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

    @property
    def total_1(self):
        # returns Term-1 total marks obtained from 100
        return self.per_test_1 + self.notebook_1 + self.sea_1 + self.main_1

    @property
    def total_2(self):
        # returns Term-2 total marks obtained from 100
        return self.per_test_2 + self.notebook_2 + self.sea_2 + self.main_2

    def save(self, *args, **kwargs):
        self.grade_1 = find_grade(self.total_1)
        self.grade_2 = find_grade(self.total_2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student.user.first_name + " ("+ self.student.stud_class + "-" + self.student.stud_section + "-" + self.student.stud_rollno + ") report"
