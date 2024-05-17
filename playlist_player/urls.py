from django.urls import path
from playlist_player.views import *

app_name = 'playlist_player'

urlpatterns = [
    path('user-playlist/', user_playlist, name='user_playlist'),
    path('tambah-playlist/', tambah_playlist, name='tambah_playlist'),
    path('detail-playlist/', detail_playlist, name='detail_playlist'),
    path('tambah-lagu/', tambah_lagu, name='tambah_lagu'),
    path('play-song/', play_song, name='play_song'),
    path('add-song-to-user-playlist/', add_song_to_user_playlist, name='add_song_to_user_playlist'),
    path('play-user-playlist/', play_user_playlist, name='play_user_playlist'),
    path('pesan-add-song-to-playlist/', pesan_add_song_to_playlist, name='pesan_add_song_to_playlist'),
    path('ubah-playlist/', ubah_playlist, name='ubah_playlist'),
    path('hapus-playlist/', hapus_playlist, name='hapus_playlist'),
    path('pesan-download-song/', pesan_download_song, name='pesan_download_song'),
]