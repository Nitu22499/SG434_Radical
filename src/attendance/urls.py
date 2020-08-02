from django.urls import path

from .views import (AttendanceIndexView, StudentAttendanceView, StudentAttendanceHomeView, EmployeeAttendanceView,
                    EmployeeAttendanceHomeView)

app_name = 'attendance'

urlpatterns = (
    path('', AttendanceIndexView.as_view(), name='index'),

    path('student/', StudentAttendanceHomeView.as_view(), name='student_home'),
    path('student/v/<slug:start_date>/<slug:end_date>/<slug:subject>/<slug:section>/', StudentAttendanceView.as_view(),
         name='student_view'),

    path('employee/', EmployeeAttendanceHomeView.as_view(), name='employee_home'),
    path('employee/v/<slug:start_date>/<slug:end_date>/', EmployeeAttendanceView.as_view(), name='employee_view'),
)
