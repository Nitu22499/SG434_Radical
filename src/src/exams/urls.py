from django.urls import path
from .views import reportView, getSubjects, saveExamForm

app_name = 'exams'


urlpatterns = [
    path('report/', reportView, name='report'),
    path('subject/class/<class_level>', getSubjects, name='subjects-list'),
    path('exam_form/save', saveExamForm, name='save-exam-form'),
]