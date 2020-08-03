from django.urls import path

from .views import (
    AttendanceIndexView, StudentAttendanceListView, StudentAttendanceHomeView, EmployeeAttendanceListView,
    EmployeeAttendanceHomeView, StudentAttendanceCreateView, StudentAttendanceUpdateView, student_mark_attendance,
    StudentAttendanceDetailView, student_attendance_delete_view, EmployeeAttendanceDetailView,
    EmployeeAttendanceCreateView, EmployeeAttendanceUpdateView, employee_mark_attendance, StudentAttendanceIdView,
    employee_attendance_delete_view, MyAttendanceFetchView, MyAttendanceDetailView, load_school, load_block
)

app_name = 'attendance'

urlpatterns = (
    path('', AttendanceIndexView.as_view(), name='index'),

    # student
    path('student/', StudentAttendanceHomeView.as_view(), name='student_home'),
    path('student/l/<slug:start_date>/<slug:end_date>/<slug:subject>/<slug:section>/<int:school>',
         StudentAttendanceListView.as_view(), name='student_view'),
    path('student/detail/<slug:create_date>/<slug:subject>/<slug:section>/<int:school>/',
         StudentAttendanceDetailView.as_view(), name='student_detail'),
    path('student/add/', StudentAttendanceCreateView.as_view(), name='student_add'),
    path('student/update/<slug:create_date>/<slug:subject>/<slug:section>/', StudentAttendanceUpdateView.as_view(),
         name='student_update'),
    path('student/delete/', student_attendance_delete_view, name='student_delete'),
    path('student/mark-attendance/<slug:create_date>/<slug:subject>/<slug:section>/', student_mark_attendance,
         name='student_mark_attendance'),

    path('student/individual/<int:pk>/', StudentAttendanceIdView.as_view(), name='student_id'),
    path('student/individual/detail/<int:student>/<slug:start_date>/<slug:end_date>/<slug:subject>/',
         MyAttendanceDetailView.as_view(), name='student_id_detail'),

    # employee
    path('employee/', EmployeeAttendanceHomeView.as_view(), name='employee_home'),
    path('employee/l/<slug:start_date>/<slug:end_date>/<int:school>', EmployeeAttendanceListView.as_view(),
         name='employee_view'),
    path('employee/detail/<slug:create_date>/<int:school>', EmployeeAttendanceDetailView.as_view(),
         name='employee_detail'),
    path('employee/add/', EmployeeAttendanceCreateView.as_view(), name='employee_add'),
    path('employee/update/<slug:create_date>/', EmployeeAttendanceUpdateView.as_view(), name='employee_update'),
    path('employee/delete/', employee_attendance_delete_view, name='employee_delete'),
    path('employee/mark-attendance/<slug:create_date>/', employee_mark_attendance, name='employee_mark_attendance'),

    # self
    path('my/', MyAttendanceFetchView.as_view(), name='my_home'),
    path('my/detail/<slug:start_date>/<slug:end_date>/<slug:subject>/', MyAttendanceDetailView.as_view(),
         name='my_detail'),

    # dropdown
    path('dropdown/school', load_school, name='load_school'),
    path('dropdown/block', load_block, name='load_block'),
)
