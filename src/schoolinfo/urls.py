from .views import  SectionsHome,SchoolProfileView,PhysicalFacilitiesView,RepeatersByGradeView,SaveRepeatersByGradeView
from django.urls import path, include

app_name = 'schoolinfo'

urlpatterns = [
    path('', SectionsHome.as_view(), name='sections_home'),
    path('school-profile', SchoolProfileView.as_view(), name='school_profile'),
    path('repeaters-by-grade', RepeatersByGradeView, name='repeaters_by_grade'),
    path('repeaters-by-grade/save', SaveRepeatersByGradeView, name='repeaters_by_grade_save'),
    path('physical-facilities', PhysicalFacilitiesView.as_view(), name='physical_facilities'),    
]