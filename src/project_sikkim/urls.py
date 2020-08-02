from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-control-panel/', admin.site.urls),
    path('', include('misc.urls')),
    path('attendance/', include('attendance.urls')),
    path('', include('profiles.urls')),
    path('exams/', include('exams.urls')),
    path('schoolinfo/', include('schoolinfo.urls')),
   
    path('emp/', include('employee.urls')),
    
    path('report/', include('reports.urls')),
]

admin.site.site_header = "Sikkim S.I.S"
admin.site.site_title = "Sikkim S.I.S"
admin.site.index_title = ""
