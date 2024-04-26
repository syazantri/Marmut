from django.urls import path
from album_royalti.views import *

app_name = 'album_royalti'

urlpatterns = [
    path('royalti/', cek_royalti, name='cek_royalti'),
    path('create-album/', create_album, name='create_album'),
    path('create-song/', create_song, name='create_song'),
    path('list-album/', list_album, name='list_album'),
    path('list-edit-album/', list_edit_album, name='list_edit_album'),
    path('list-song/', list_song, name='list_song')
]