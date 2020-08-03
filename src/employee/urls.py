from django.urls import path

from .views import (EmployeeCreateView, TeacherCreateView, EmployeeListView, EmployeeDetailView, EmployeeDeleteView,
                    EmployeeUpdateView, EmployeeAuthorityHomeView)

app_name = 'employee'

urlpatterns = (
    path('add/', EmployeeCreateView.as_view(), name='add'),
    path('update/<int:pk>', EmployeeUpdateView.as_view(), name='update'),
    path('teacher/add/<int:pk>', TeacherCreateView.as_view(), name='teacher_add'),
    path('teacher/update/<int:pk>', TeacherCreateView.as_view(), name='teacher_update'),
    path('authority/', EmployeeAuthorityHomeView.as_view(), name='authority'),
    path('list/', EmployeeListView.as_view(), name='list'),
    path('list/<int:school>', EmployeeListView.as_view(), name='list_with_school'),
    path('d/<int:pk>', EmployeeDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', EmployeeDeleteView.as_view(), name='delete'),
)
