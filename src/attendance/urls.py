from django.urls import path

from .views import (AttendanceHomeView, StudentAttendanceCreateView, StudentAttendanceListView,
                    StudentAttendanceDetailView, StudentAttendanceUpdateView, mark_attendance,
                    EmployeeAttendanceUpdateView, EmployeeAttendanceCreateView, EmployeeAttendanceDetailView,
                    EmployeeAttendanceListView, StudentAttendanceDeleteView, EmployeeAttendanceDeleteView)

app_name = 'attendance'

urlpatterns = (
    path('', AttendanceHomeView.as_view(), name='home'),

    path('student/', StudentAttendanceListView.as_view(), name='student-list'),
    path('student/<int:pk>', StudentAttendanceDetailView.as_view(), name='student-detail'),
    path('student/create', StudentAttendanceCreateView.as_view(), name='student-create'),
    path('student/update/<int:pk>', StudentAttendanceUpdateView.as_view(), name='student-update'),
    path('student/mark_attendance/<int:pk>', mark_attendance, name='student-mark-attendance'),
    path('student/delete/<int:pk>', StudentAttendanceDeleteView.as_view(), name='student-delete'),

    path('employee/', EmployeeAttendanceListView.as_view(), name='employee-list'),
    path('employee/<int:pk>', EmployeeAttendanceDetailView.as_view(), name='employee-detail'),
    path('employee/create', EmployeeAttendanceCreateView.as_view(), name='employee-create'),
    path('employee/update/<int:pk>', EmployeeAttendanceUpdateView.as_view(), name='employee-update'),
    path('employee/mark_attendance/<int:pk>', mark_attendance, name='employee-mark-attendance'),
    path('employee/delete/<int:pk>', EmployeeAttendanceDeleteView.as_view(), name='employee-delete'),
)
