from django.urls import path
from .views import ReportHome, SchoolsByMgmt

app_name = 'reports'

urlpatterns = [
    path('', ReportHome.as_view(), name = 'reports_home'),
    path('schools-by-mgmt/', SchoolsByMgmt.as_view(), name = 'schools_by_mgmt'),    
    # path('student-list/', StudentList.as_view(), name = 'student-list'),
    # path('student-list/<int:stud>', StudentInfo.as_view(), name = 'student-info'),

    
]