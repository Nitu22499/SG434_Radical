from django.urls import path


from .views import DashboardView, chart, get_blocks_by_district, get_attendance_data, get_academic_data, index


urlpatterns = [
    path('school_dashboard/', DashboardView.as_view(), name='school_dashboard'),
    path('chart/', chart, name='chart'),
    path('get-blocks/', get_blocks_by_district, name='get_blocks'),
    path('get-attendance/', get_attendance_data, name='get_attendance'),
    path('get-academic-data/', get_academic_data, name='get_academic_data'),
    path('home/', index, name='landing_page')
]
