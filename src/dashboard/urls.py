from django.urls import path


from .views import DashboardView


urlpatterns = [
    path('school_dashboard/', DashboardView.as_view(), name='school_dashboard'),
]
