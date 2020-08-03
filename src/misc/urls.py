from django.urls import path, include
from .views import Home, LandingPage, load_blocks

app_name = 'misc'

urlpatterns = [
    path('', Home.as_view(), name = "home"),
    path('lp/', LandingPage.as_view(), name = "landing-page"),
    path('ajax/load-blocks/', load_blocks, name='ajax_load_blocks'),
]