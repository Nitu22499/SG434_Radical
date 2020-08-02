from django.urls import path
from .views import reportView, getSubjects, saveExamForm, saveExamFormCoScholastic, studentReportView

app_name = 'exams'


urlpatterns = [
    path('report/edit', reportView, name='report'),
    path('report/student-view', studentReportView, name='student-report'),
    path('subject/class/<class_level>', getSubjects, name='subjects-list'),
    path('exam_form/save', saveExamForm, name='save-exam-form'),
    path('exam_form_co_scholastic/save', saveExamFormCoScholastic, name='save-exam-form-co-scholastic'),
]