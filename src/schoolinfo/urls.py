from django.urls import path, include
from .views import SectionsHome, SchoolProfileView, RepeatersByGradeView

app_name = 'schoolinfo'

urlpatterns = [
    path('', SectionsHome.as_view(), name='sections_home'),
    path('school-profile', SchoolProfileView.as_view(), name='school_profile'),
    path('repeaters-by-grade', RepeatersByGradeView, name='repeaters_by_grade')
]