from django.shortcuts import render
from utils.query import *

def homepage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    email = request.COOKIES.get('email')

    cursor.execute(
        f'select * from akun where email = \'{email}\'')
    user = cursor.fetchmany()

    isArtist = False
    isSongwriter = False
    isPodcaster = False
    id_artist = ""
    id_songwriter = ""
    id_pemilik_hak_cipta_artist = ""
    id_pemilik_hak_cipta_songwriter = ""
    status_langganan = "NonPremium"
    records_song_artist = []
    records_song_songwriter = []
    records_podcast = []

    # Cari, apakah dia artist?
    cursor.execute(
        f'select * from artist where email_akun = \'{email}\'')
    artist = cursor.fetchmany()
    if len(artist) == 1:
        isArtist = True
        id_artist = artist[0][0] 
        id_pemilik_hak_cipta_artist = artist[0][2]
        # Cari lagu artist
        cursor.execute(
            f'select * from song where id_artist = \'{id_artist}\'')
        records_song_artist_awal = cursor.fetchall()
        for song in records_song_artist_awal:
            id_song = song[0]
            cursor.execute(
                f'select judul, durasi from konten where id = \'{id_song}\'')
            additional_detail_song = cursor.fetchone()
            if additional_detail_song:
                updated_song = song + additional_detail_song
                records_song_artist.append(updated_song)

    # Cari, apakah dia songwriter?
    cursor.execute(
        f'select * from songwriter where email_akun = \'{email}\'')
    songwriter = cursor.fetchmany()
    if len(songwriter) == 1:
        isSongwriter = True
        id_songwriter = songwriter[0][0] 
        id_pemilik_hak_cipta_songwriter = songwriter[0][2]
        # Cari lagu songwriter
        cursor.execute(
            f'select id_song from songwriter_write_song where id_songwriter = \'{id_songwriter}\'')
        list_id_song = cursor.fetchall()
        if len(list_id_song) != 0 :
            records_song_songwriter = []
            for song in list_id_song:
                id_song = song[0]
                cursor.execute(
                    f'select * from song where id_konten = \'{id_song}\'')
                records_song_awal = cursor.fetchone()
                cursor.execute(
                    f'select judul, durasi from konten where id = \'{id_song}\'')
                additional_detail_song = cursor.fetchone()
                records_song_songwriter.append(records_song_awal + additional_detail_song)

    # Cari, apakah dia podcaster?
    cursor.execute(
        f'select * from podcaster where email = \'{email}\'')
    podcaster = cursor.fetchmany()
    if len(podcaster) == 1:
        isPodcaster = True
        # Cari podcastnya podcaster
        cursor.execute(
            f'select * from podcast where email_podcaster = \'{email}\'')
        list_id_podcast = cursor.fetchall()
        if len(list_id_podcast) != 0:
            records_podcast = []
            for podcast in list_id_podcast:
                id_podcast = podcast[0]
                cursor.execute(
                    f'SELECT k.id, k.judul, COUNT(*) AS jumlah_episode, k.durasi FROM KONTEN AS k JOIN EPISODE AS e ON e.id_konten_podcast = k.id where k.id = \'{podcast[0]}\' GROUP BY k.id')
                records_podcast.append(cursor.fetchone())

    # Semua pengguna pasti pengguna biasa juga yang bisa punya userplaylist
    cursor.execute(
        f'select * from user_playlist where email_pembuat = \'{email}\'')
    records_user_playlist = cursor.fetchall()
        
    # Cek dia user premium atau nonpremium
    cursor.execute(
        f'select * from premium where email = \'{email}\'')
    premium = cursor.fetchall()
    if len(premium) != 0:
        status_langganan = "Premium"

    # Assign role verified
    role_verified_list = []
    if(isArtist == True):
        role_verified_list.append('Artist')
    if(isSongwriter == True):
        role_verified_list.append('Songwriter')
    if(isPodcaster == True):
        role_verified_list.append('Podcast')
    if len(role_verified_list) == 0 :
        role_verified = "Pengguna Biasa"
    else:
        role_verified = ', '.join(role_verified_list)

    context = {
        'role': 'pengguna',
        'status': 'success',
        'role_verified': role_verified,
        'nama': user[0][2],
        'email': user[0][0],
        'status_langganan': status_langganan,
        'kota_asal': user[0][7],
        'gender': user[0][3],
        'tempat_lahir': user[0][4],
        'tanggal_lahir': user[0][5],
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'isPodcaster': isPodcaster,
        'records_user_playlist': records_user_playlist,
        'records_song_artist': records_song_artist,
        'records_song_songwriter': records_song_songwriter,
        'records_podcast': records_podcast,
    }
    response = render(request, 'dashboard_pengguna.html', context)
    # response.set_cookie('role', 'pengguna')
    # response.set_cookie('statusLangganan', status_langganan)
    # response.set_cookie('isArtist', isArtist)
    # response.set_cookie('isSongwriter', isSongwriter)
    # response.set_cookie('isPodcaster', isPodcaster)
    # response.set_cookie('email', email)
    # response.set_cookie('idArtist', id_artist)
    # response.set_cookie('idSongwriter', id_songwriter)
    # response.set_cookie('idPemilikCiptaArtist', id_pemilik_hak_cipta_artist)
    # response.set_cookie('idPemilikCiptaSongwriter', id_pemilik_hak_cipta_songwriter)
    return response
    return render(request, 'dashboard_pengguna.html')

def dashboard_label(request):
    email = request.COOKIES.get('email')

    cursor.execute(
        f'select * from label where email = \'{email}\'')
    label = cursor.fetchmany()
    if len(label) == 1 :
        #Cari album yang dimiliki label
        id_label = label[0][0]
        cursor.execute(
            f'select * from album where id_label = \'{id_label}\'')
        records_album = cursor.fetchall()
        context = {
            'role': 'label',
            'status': 'success',
            'id': label[0][0],
            'nama': label[0][1],
            'email': label[0][2],
            'kontak': label[0][4],
            'id_pemilik_hak_cipta': label[0][5],
            'records_album': records_album,
        }
        response = render(request, 'dashboard_label.html', context)
        # response.set_cookie('role', 'label')
        # response.set_cookie('email', label[0][1])
        # response.set_cookie('id', label[0][0])
        # response.set_cookie('idPemilikCiptaLabel', label[0][5])
        return response
    
    return render(request, 'dashboard_label.html')