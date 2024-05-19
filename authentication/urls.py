from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', main_register, name='main_register'),
    path('register-label/', register_label, name='register_label'),
    path('register-biasa/', register_pengguna, name='register_pengguna')
]