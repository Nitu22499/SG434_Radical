from django.urls import path, include
from .views import Home

app_name = 'misc'

urlpatterns = [
    path('', Home.as_view(), name = "home"),
    
]