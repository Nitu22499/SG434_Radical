from django.urls import path
from .views import ReportHome, SchoolsByMgmt
from .viewsk import TypeOfSchool, SchoolsByArea, TeachersBySchoolCategory, TeachersBySocialCategory

app_name = 'reports'

urlpatterns = [
    path('', ReportHome.as_view(), name = 'reports_home'),
    path('schools-by-mgmt/', SchoolsByMgmt.as_view(), name = 'schools_by_mgmt'),    
    path('schools-by-type/', TypeOfSchool.as_view(), name = 'schools_by_type'),    
    path('schools-by-area/', SchoolsByArea.as_view(), name = 'schools_by_area'),    
    path('teachers-by-school-category/', TeachersBySchoolCategory.as_view(), name = 'teachers_by_school_category'),    
    path('teachers-by-social-category/', TeachersBySocialCategory.as_view(), name = 'teachers_by_social_category'),    
    # path('student-list/', StudentList.as_view(), name = 'student-list'),
    # path('student-list/<int:stud>', StudentInfo.as_view(), name = 'student-info'),
]