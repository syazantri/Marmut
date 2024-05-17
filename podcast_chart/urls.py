from django.urls import path
from podcast_chart.views import *

app_name = 'podcast_chart'

urlpatterns = [
    path('play-podcast/', play_podcast, name='play_podcast'),
    path('create-podcast/', create_podcast, name='create_podcast'),
    path('lihat-chart/', lihat_chart, name='lihat_chart'),
    path('detail-chart/', detail_chart, name='detail_chart'),
    path('list-podcast/', list_podcast, name='list_podcast'),
    path('create-episode/', create_episode, name='create_episode'),
    path('list-episode/', list_episode, name='list_episode'),
    path('delete-podcast/', delete_podcast, name='delete_podcast'),
    path('delete-episode/', delete_episode, name='delete_episode'),
]
