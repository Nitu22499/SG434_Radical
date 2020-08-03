from django.urls import path
from .views import reportView, getSubjects, saveExamForm, saveExamFormCoScholastic, studentReportView, studentReportViewByID, getSchoolsByBlock, getBlocksByDistrict 

app_name = 'exams'


urlpatterns = [
    path('report/edit', reportView, name='report'),
    path('report/student-view', studentReportView, name='student-report'),
    path('report/student-view/<int:stud_id>', studentReportViewByID, name='student-report-id'),
    path('subject/class/<class_level>', getSubjects, name='subjects-list'),
    path('schools/block/<block_id>', getSchoolsByBlock, name='schools-list-block'),
    path('schools/district/<district_id>', getBlocksByDistrict, name='blocks-list-district'),
    path('exam_form/save', saveExamForm, name='save-exam-form'),
    path('exam_form_co_scholastic/save', saveExamFormCoScholastic, name='save-exam-form-co-scholastic'),
]