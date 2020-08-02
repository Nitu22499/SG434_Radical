from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-control-panel/', admin.site.urls),
    path('', include('misc.urls')),
    path('', include('profiles.urls')),
    path('exams/', include('exams.urls')),
    path('attendance/', include('attendance.urls')),
    path('profiles/', include('profiles.urls')),
    path('schoolinfo/', include('schoolinfo.urls'))
]
