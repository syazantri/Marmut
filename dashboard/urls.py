from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard-label/', dashboard_label, name='dashboard_label'),
    path('dashboard-artist-songwriter/', dashboard_artist_songwriter, name='dashboard_artist_songwriter'),
    path('dashboard-podcaster/', dashboard_podcaster, name='dashboard_podcaster')
]