from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-control-panel/', admin.site.urls),
    path('', include('misc.urls')),
    path('profiles/', include('profiles.urls')),
    path('schoolinfo/', include('schoolinfo.urls'))
    
]
