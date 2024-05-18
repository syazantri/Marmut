from django.urls import path
from premium_search.views import *

app_name = 'premium_search'

urlpatterns = [
    path('langganan/', cek_langganan ,name='cek_langganan'),
    path('downloaded/', downloaded_song ,name='downloaded_song'),
    path('search/',search_bar,name='search_bar'),
    path('delete/',delete,name='delete'),
    path('payment/',payment,name='payment'),
    path('riwayat/',riwayat,name='riwayat'),
    path('process_payment/', process_payment, name='process_payment'),
]