from .viewsk import *
from .views import  *
from .views2 import *
from django.urls import path, include

app_name = 'schoolinfo'

urlpatterns = [
    path('repeaters-by-grade', RepeatersByGradeView, name='repeaters_by_grade'),
    path('repeaters-by-grade/save', SaveRepeatersByGradeView, name='repeaters_by_grade_save'),
    path('<str:ac_year>', SectionsHome.as_view(), name='sections_home'),
    path('school-profile/<str:ac_year>', SchoolProfileView.as_view(), name='school_profile'),    
    path('physical-facilities/<str:ac_year>', PhysicalFacilitiesView.as_view(), name='physical_facilities'),    
    path('school-rte/<str:ac_year>',SchoolRTEView,name='school_rte'),
    path('school-rte/<str:ac_year>/save',SaveSchoolRTEView,name='school_rte_save'),
    path('school-ews/<str:ac_year>',SchoolEWSView,name='school_ews'),
    path('school-ews/<str:ac_year>/save',SaveSchoolEWSView,name='school_ews_save'),
    path('school-profile-details/<int:pk>',ProfileDetailView.as_view(),name='school_profile_details'),
    path('government-details/<int:pk>',GovernmentDetailView.as_view(),name='school_government_details'),
    path('physical-details/<int:pk>',PhysicalDetailView.as_view(),name='school_physical_details'),
    path('school-rte-details/<str:ac_year>',SchoolRTEDetailView,name='school_rte_details'),
    path('school-ews-details/<str:ac_year>',SchoolEWSDetailView,name='school_ews_details'),
    path('school-incentives-details/<str:ac_year>',SchoolIncentivesDetailView,name='school_incentives_details'),
    path('school-library/<str:ac_year>',SchoolLibraryView.as_view(),name='school_library'),
    path('library-details/<int:pk>',SchoolLibraryDetailView.as_view(),name='library_details'),
    path('school-items/<str:ac_year>',SchoolItemsView.as_view(),name='school_items'),
    path('items-details/<int:pk>',SchoolItemsDetailView.as_view(),name='items_details'),
    path('school-toilets/<str:ac_year>',SchoolToiletView.as_view(),name='school_toilets'),
    path('school-toilet-details/<int:pk>',SchoolToiletDetailView.as_view(),name='toilet_details'),
    path('enrolment-pre-primary/<str:ac_year>', enrolmentPrePrimaryView, name="enrolment_pre_primary"),
    path('enrolment-pre-primary/<str:ac_year>/save', saveEnrolmentPrePrimaryView, name="save_enrolment_pre_primary"),
    path('enrolment-social-category/<str:ac_year>', enrolmentBySocialCategoryView, name="enrolment_social_category"),
    path('enrolment-by-age/<str:ac_year>', enrolmentByGradeView, name="enrolment_by_age"),
    path('enrolment-social-category/<str:ac_year>/save', saveEnrolmentBySocialCategoryView, name="enrolment_social_category_save"),
    path('enrolment-by-age/<str:ac_year>/save', saveEnrolmentByGradeView, name="enrolment_by_age_save"),
    path('school-safety/<str:ac_year>',SchoolSafetyView.as_view(),name='school_safety'),
    path('school-safety-details/<int:pk>',SchoolSafetyDetailView.as_view(),name='safety_details'),
    path('school-receipt/<str:ac_year>',SchoolReceiptView.as_view(),name='school_receipt'),
    path('school-receipt-details/<int:pk>',SchoolReceiptDetailView.as_view(),name='receipt_details'),
    path('school-incentives/',SchoolIncentivesView,name='school_incentives'),
    path('school-incentives/save',SaveSchoolIncentivesView,name='school_incentives_save'),
    path('school-annual/',SchoolAnnualView,name='school_annual'),
    path('school-annual/save',SaveSchoolAnnualView,name='school_annual_save'),
    path('school-annual-details/<str:ac_year>',SchoolAnnualDetailView,name='school_annual_details'),
]