from django.contrib import admin
from django import forms
from .models import Exam, ExamCoScholastic
from profiles.models import Subject

class CustomExamModelForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomExamModelForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(subject_type='Scholastic')

class ExamAdmin(admin.ModelAdmin):
    form = CustomExamModelForm

class CustomExamCSModelForm(forms.ModelForm):
    class Meta:
        model = ExamCoScholastic
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomExamCSModelForm, self).__init__(*args, **kwargs)
        self.fields['exam_cs_subject'].queryset = Subject.objects.filter(subject_type='Co -Scholastic')

class ExamCSAdmin(admin.ModelAdmin):
    form = CustomExamCSModelForm

# Register your models here.
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamCoScholastic, ExamCSAdmin)