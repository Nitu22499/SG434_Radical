from django.urls import path

from .views import EmployeeCreateView, TeacherCreateView, EmployeeListView, EmployeeDetailView, EmployeeDeleteView

app_name = 'employee'

urlpatterns = (
    path('add/', EmployeeCreateView.as_view(), name='add'),
    path('teacher/add/<int:pk>', TeacherCreateView.as_view(), name='teacher_add'),
    path('list/', EmployeeListView.as_view(), name='list'),
    path('d/<int:pk>', EmployeeDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', EmployeeDeleteView.as_view(), name='delete'),
)
