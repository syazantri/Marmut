from django.urls import path
from dashboard.views import *

app_name = 'dashboard'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard-label/', dashboard_label, name='dashboard_label'),
]