from django.urls import path

from .views import (
    AttendanceIndexView, StudentAttendanceListView, StudentAttendanceHomeView, EmployeeAttendanceListView,
    EmployeeAttendanceHomeView, StudentAttendanceCreateView, StudentAttendanceUpdateView, student_mark_attendance,
    StudentAttendanceDetailView, student_attendance_delete_view, EmployeeAttendanceDetailView,
    EmployeeAttendanceCreateView, EmployeeAttendanceUpdateView, employee_mark_attendance,
    employee_attendance_delete_view
)

app_name = 'attendance'

urlpatterns = (
    path('', AttendanceIndexView.as_view(), name='index'),

    # student
    path('student/', StudentAttendanceHomeView.as_view(), name='student_home'),
    path('student/l/<slug:start_date>/<slug:end_date>/<slug:subject>/<slug:section>/',
         StudentAttendanceListView.as_view(), name='student_view'),
    path('student/detail/<slug:create_date>/<slug:subject>/<slug:section>/', StudentAttendanceDetailView.as_view(),
         name='student_detail'),
    path('student/add/', StudentAttendanceCreateView.as_view(), name='student_add'),
    path('student/update/<slug:create_date>/<slug:subject>/<slug:section>/', StudentAttendanceUpdateView.as_view(),
         name='student_update'),
    path('student/delete/', student_attendance_delete_view, name='student_delete'),
    path('student/mark-attendance/<slug:create_date>/<slug:subject>/<slug:section>/', student_mark_attendance,
         name='student_mark_attendance'),

    # employee
    path('employee/', EmployeeAttendanceHomeView.as_view(), name='employee_home'),
    path('employee/l/<slug:start_date>/<slug:end_date>/', EmployeeAttendanceListView.as_view(), name='employee_view'),
    path('employee/detail/<slug:create_date>/', EmployeeAttendanceDetailView.as_view(), name='employee_detail'),
    path('employee/add/', EmployeeAttendanceCreateView.as_view(), name='employee_add'),
    path('employee/update/<slug:create_date>/', EmployeeAttendanceUpdateView.as_view(), name='employee_update'),
    path('employee/delete/', employee_attendance_delete_view, name='employee_delete'),
    path('employee/mark-attendance/<slug:create_date>/', employee_mark_attendance, name='employee_mark_attendance'),
)
