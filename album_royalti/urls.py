from django.urls import path
from dashboard.views import homepage

app_name = 'dashboard'

urlpatterns = [
    path('', homepage, name='homepage')
]