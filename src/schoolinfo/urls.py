from .views import  SectionsHome,SchoolProfileView,PhysicalFacilitiesView,RepeatersByGradeView,SaveRepeatersByGradeView,SchoolRTEView,SaveSchoolRTEView,SchoolItemsView
from .views import SchoolLibraryDetailView,ProfileDetailView,GovernmentDetailView,PhysicalDetailView,SchoolRTEDetailView,SchoolEWSView,SaveSchoolEWSView,SchoolEWSDetailView,SchoolLibraryView
from .views import SchoolItemsDetailView,SchoolToiletView,SchoolToiletDetailView
from django.urls import path, include

app_name = 'schoolinfo'

urlpatterns = [
    path('<str:ac_year>', SectionsHome.as_view(), name='sections_home'),
    path('school-profile/<str:ac_year>', SchoolProfileView.as_view(), name='school_profile'),
    path('repeaters-by-grade', RepeatersByGradeView, name='repeaters_by_grade'),
    path('repeaters-by-grade/save', SaveRepeatersByGradeView, name='repeaters_by_grade_save'),
    path('physical-facilities/<str:ac_year>', PhysicalFacilitiesView.as_view(), name='physical_facilities'),    
    path('school-rte/<str:ac_year>',SchoolRTEView,name='school_rte'),
    path('school-rte/<str:ac_year>/save',SaveSchoolRTEView,name='school_rte_save'),
    path('school-ews/<str:ac_year>',SchoolEWSView,name='school_ews'),
    path('school-ews/<str:ac_year>/save',SaveSchoolEWSView,name='school_ews_save'),
    path('school-profile-details/<int:pk>',ProfileDetailView.as_view(),name='school_profile_details'),
    path('government-details/<int:pk>',GovernmentDetailView.as_view(),name='school_government_details'),
    path('physical-details/<int:pk>',PhysicalDetailView.as_view(),name='school_physical_details'),
    path('school-rte-details/<int:pk>',SchoolRTEDetailView,name='school_rte_details'),
    path('school-ews-details/<int:pk>',SchoolEWSDetailView,name='school_ews_details'),
    path('school-library/<str:ac_year>',SchoolLibraryView.as_view(),name='school_library'),
    path('library-details/<int:pk>',SchoolLibraryDetailView.as_view(),name='library_details'),
    path('school-items/<str:ac_year>',SchoolItemsView.as_view(),name='school_items'),
    path('items-details/<int:pk>',SchoolItemsDetailView.as_view(),name='items_details'),
    path('school-toilets/<str:ac_year>',SchoolToiletView.as_view(),name='school_toilets'),
    path('school-toilet-details/<int:pk>',SchoolToiletDetailView.as_view(),name='toilet_details'),
]