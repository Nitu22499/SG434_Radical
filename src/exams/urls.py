from django.urls import path
from .views import reportView, getSubjects

app_name = 'exams'


urlpatterns = [
    path('report/', reportView, name='report'),
    path('subject/class/<class_level>', getSubjects, name='subjects-list'),
]