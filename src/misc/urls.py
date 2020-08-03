from django.urls import path, include
from .views import Home, load_blocks

app_name = 'misc'

urlpatterns = [
    path('home/', Home.as_view(), name = "home"),
    path('ajax/load-blocks/', load_blocks, name='ajax_load_blocks'),
    
]