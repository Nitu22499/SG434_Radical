from django.urls import path


from .views import DashboardView, chart, get_blocks_by_district, home_view


urlpatterns = [
    path('school_dashboard/', DashboardView.as_view(), name='school_dashboard'),
    path('chart/', chart, name='chart'),
    path('get-blocks/', get_blocks_by_district, name='get_blocks'),
    path('home/', home_view, name='home')
]
