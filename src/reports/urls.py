from django.urls import path
from .views import ReportHome, SchoolsByMgmt
from .viewsk import *
from .viewsp import *

app_name = 'reports'

urlpatterns = [
    path('', ReportHome.as_view(), name = 'reports_home'),
    path('schools-by-mgmt/', SchoolsByMgmt.as_view(), name = 'schools_by_mgmt'),   
    path('schools-by-ab/', SchoolsByab.as_view(), name = 'schools_by_ab'),   
    path('schools-by-ct/', SchoolsByct.as_view(), name = 'schools_by_ct'),  
    path('schools-by-sb/', SchoolsBysb.as_view(), name = 'schools_by_sb'),  
    path('schools-by-bw/', SchoolsBybw.as_view(), name = 'schools_by_bw'),    
    path('schools-by-ec/', SchoolsByec.as_view(), name = 'schools_by_ec'), 
    path('schools-by-cwsn/', SchoolsBycwsn.as_view(), name = 'schools_by_cwsn'),    
    path('schools-by-if/', SchoolsByif.as_view(), name = 'schools_by_if'),   
    path('schools-by-c/', SchoolsByc.as_view(), name = 'schools_by_c'),   
    path('schools-by-type/', TypeOfSchool.as_view(), name = 'schools_by_type'),    
    path('schools-by-area/', SchoolsByArea.as_view(), name = 'schools_by_area'),    
    path('students-enrolment-by-area/', StudentsEnrolmentByArea.as_view(), name = 'students_enrolment_by_area'),    
    path('teachers-by-school-category/', TeachersBySchoolCategory.as_view(), name = 'teachers_by_school_category'),    
    path('teachers-by-social-category/', TeachersBySocialCategory.as_view(), name = 'teachers_by_social_category'),    
    path('students-by-social-category/', StudentsBySocialCategory.as_view(), name = 'students_enrolment_by_social_category'),    
    path('teachers-received-in-service-training/', TeachersReceivedInServiceTraining.as_view(), name = 'teachers_received_in_service_training'),    
    path('teachers-trained-for-cwsn/', TeachersTrainedForCWSN.as_view(), name = 'teachers_trained_for_cwsn'),    
    path('students-enrolment-by-mgmt-category/', StudentsEnrolmentByMgmtCategory.as_view(), name = 'students_enrolment_by_mgmt_category'),    
    path('students-enrolment-by-gender/', StudentsEnrolmentByGender.as_view(), name = 'students_enrolment_by_gender'),    
    path('students-received-free-textbooks/', StudentsReceivedFreeTextbooks.as_view(), name = 'students_received_free_textbooks'),    
    # path('student-list/', StudentList.as_view(), name = 'student-list'),
    # path('student-list/<int:stud>', StudentInfo.as_view(), name = 'student-info'),
]