from django.urls import path
from podcast_chart.views import *

app_name = 'podcast_chart'

urlpatterns = [
    path('play_podcast/', play_podcast, name='play_podcast'),
    path('play_user_playlist/', play_user_playlist, name='play_user_playlist'),
    path('lihat_chart/', lihat_chart, name='lihat_chart'),
    path('detail_chart/', detail_chart, name='detail_chart'),
]
