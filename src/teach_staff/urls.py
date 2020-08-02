app_name = 'teach_staff'
from django.urls import path, include
from teach_staff.views import (Teaching_Staff_InfoListView, Teaching_Staff_InfoDetailView,
                                Teaching_Staff_InfoDeleteView, Teaching_Staff_InfoCreateView, 
                                Teaching_Staff_InfoUpdateView, Teaching_Staff_TemplateView,
                                Teaching_Staff_NonTeachers_InfoListView, Teaching_Staff_NonTeachers_InfoDetailView,
                                Teaching_Staff_NonTeachers_InfoCreateView, Teaching_Staff_NonTeachers_InfoUpdateView,
                                Teaching_Staff_NonTeachers_InfoDeleteView)
urlpatterns = [
    path('Teachers_and_Staff_List/', Teaching_Staff_InfoListView.as_view(), name = 'Teacher_List'),
    path('Teachers_and_Staff_List/<int:pk>', Teaching_Staff_InfoDetailView.as_view(), name = 'Teacher_Detail'),
    path('create/', Teaching_Staff_InfoCreateView.as_view(), name = 'Teacher_Create'),
    path('Teachers_and_Staff_List/update/<int:pk>', Teaching_Staff_InfoUpdateView.as_view(), name = 'Teacher_Update'),
    path('Teachers_and_Staff_List/delete/<int:pk>', Teaching_Staff_InfoDeleteView.as_view(), name = 'Teacher_Delete'),
    path('', Teaching_Staff_TemplateView.as_view(), name = 'HomePage'),
    ####################################################################

    path('NonTeachers_List/', Teaching_Staff_NonTeachers_InfoListView.as_view(), name = 'NonTeachers_List'),
    path('NonTeachers_List/<int:pk>', Teaching_Staff_NonTeachers_InfoDetailView.as_view(), name = 'NonTeachers_Detail'),
    path('NonTeachers_Create/', Teaching_Staff_NonTeachers_InfoCreateView.as_view(), name = 'NonTeachers_Create'),
    path('NonTeachers_List/update/<int:pk>', Teaching_Staff_NonTeachers_InfoUpdateView.as_view(), name = 'NonTeachers_Update'),
    path('NonTeachers_List/delete/<int:pk>', Teaching_Staff_NonTeachers_InfoDeleteView.as_view(), name = 'NonTeachers_Delete'),

    
]
