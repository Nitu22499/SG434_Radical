from .views import SectionsHome, SchoolProfileView,PhysicalFacilitiesView
from django.urls import path, include


app_name = 'schoolinfo'

urlpatterns = [
    path('', SectionsHome.as_view(), name='sections_home'),
    path('school-profile', SchoolProfileView.as_view(), name='school_profile'),
    path('physical-facilities', PhysicalFacilitiesView.as_view(), name='physical_facilities'),
    
]