import json
import uuid
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import *
from datetime import datetime

def user_playlist(request):
    email = request.COOKIES.get('email')
    records_playlist = []

    cursor.execute(
        f'SELECT * from user_playlist where email_pembuat = \'{email}\'')
    records_playlist = cursor.fetchall()
    context = {
        'status': 'success',
        'records_playlist': records_playlist
    }
    response = render(request, 'user_playlist.html', context)
    return response

def tambah_playlist(request):
    email = request.COOKIES.get('email')
    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        id_playlist = str(uuid.uuid4())
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')

        # insert ke tabel playlist
        cursor.execute(
            f'insert into playlist values (\'{id_playlist}\')')

        # #insert ke tabel user_playlist
        cursor.execute(
            f'insert into user_playlist values (\'{email}\', \'{id_playlist}\', \'{judul}\', \'{deskripsi}\', 0, \'{date_now}\', \'{id_playlist}\', 0)')
        
        connection.commit()
        return redirect('playlist_player:user_playlist')

    return render(request, 'tambah_playlist.html')

def detail_playlist(request):
    playlist_id = request.GET.get('playlist_id')
    records_playlist = []
    records_song = []
    email = request.COOKIES.get('email')

    cursor.execute(
        f'SELECT * from user_playlist where id_playlist = \'{playlist_id}\'')
    records_playlist = cursor.fetchall()

    cursor.execute(
        f'SELECT id_song from playlist_song where id_playlist = \'{playlist_id}\'')
    records_song = cursor.fetchall()
    for i in range(len(records_song)):
        cursor.execute(
            f'SELECT judul, akun.nama, durasi, konten.id from konten, song, artist, akun where konten.id = \'{records_song[i][0]}\' AND konten.id = song.id_konten AND id_artist = artist.id AND artist.email_akun = akun.email')
        records_song[i] = records_song[i] + cursor.fetchone()
    
    if request.method == 'POST':
        if 'shuffle_play' in request.POST:
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert ke tabel AKUN_PLAY_PLAYLIST 
            cursor.execute(
                f'INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu) '
                f'VALUES (\'{email}\', \'{records_playlist[0][1]}\', \'{records_playlist[0][0]}\', \'{current_timestamp}\')')

            connection.commit()
   
            # Insert ke tabel AKUN_PLAY_SONG untuk setiap lagu dalam playlist 
            test = 0
            for i in range((len(records_song)//2)-1):
                id = records_song[i][0] 
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    f'INSERT INTO akun_play_song (email_pemain, id_song, waktu) '
                    f'VALUES (\'{email}\', \'{id}\', \'{current_timestamp}\')')
                test += 1
                if test > (len(records_song)//2):
                    break
        
            connection.commit()
            
            return redirect(reverse("playlist_player:play_user_playlist") + f'?playlist_id={playlist_id}')
        
        else: 
            for song in records_song:
                song_id = song[0]
                if f'play_song_{song_id}' in request.POST:
                    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(
                        f'INSERT INTO akun_play_song (email_pemain, id_song, waktu) '
                        f'VALUES (\'{email}\', \'{song_id}\', \'{current_timestamp}\')')

                    connection.commit()
                    url = reverse('playlist_player:play_song')
                    url_with_params = f"{url}?song_id={song_id}"
                    return redirect(url_with_params)

    total_durasi_menit = records_playlist[0][7]
    total_jam = total_durasi_menit // 60
    total_menit = total_durasi_menit % 60
    total_durasi_format = f'{total_jam} jam {total_menit} menit'
 
    context = {
        'status': 'success',
        'records_playlist': records_playlist,
        'records_song': records_song,
        'playlist_id': playlist_id,
        'total_durasi_format': total_durasi_format
    }
    response = render(request, 'detail_playlist.html', context)
    response.set_cookie('playlist_id', playlist_id)
    return response

def tambah_lagu(request):
    playlist_id = request.GET.get('playlist_id')
    list_lagu = []
    email = request.COOKIES.get('email')

    if request.method == 'POST' and not request.method == 'GET':
        lagu = request.POST.get('lagu')
        try:
            ada = []
            cursor.execute(
                f'select * from playlist_song where id_playlist = \'{playlist_id}\' AND id_song = \'{lagu}\''
            )
            ada = cursor.fetchall()
            if len(ada) > 0:
                return render(request, 'song_telah_ditambahkan.html')
            
            cursor.execute(
                f'insert into playlist_song values (\'{playlist_id}\', \'{lagu}\')')
            
            connection.commit()
            url = reverse('playlist_player:detail_playlist')
            url_with_params = f"{url}?playlist_id={playlist_id}"
            return redirect(url_with_params)
        
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
        # return redirect('playlist_player:detail_playlist')

    cursor.execute(
        f'select song.id_konten, akun.nama, konten.judul from konten, song, artist, akun where konten.id = song.id_konten AND song.id_artist = artist.id AND artist.email_akun = akun.email')
    list_lagu = cursor.fetchall()

    context = {
        'list_lagu': list_lagu,
        'playlist_id': playlist_id
    }
    return render(request, 'tambah_lagu.html', context)

def play_song(request):
    song_id = request.GET.get('song_id')
    records_song = []
    records_genre = []
    records_songwriter = []
    email = request.COOKIES.get('email')
    isPremium = request.COOKIES.get('statusLangganan')

    cursor.execute(
        f'SELECT * from konten where id = \'{song_id}\'')
    records_song = cursor.fetchall()

    cursor.execute(
        f'SELECT akun.nama from akun, song, artist where song.id_konten = \'{song_id}\' AND song.id_artist = artist.id AND artist.email_akun = akun.email')
    records_song[0] = records_song[0] + cursor.fetchone()

    cursor.execute(
        f'SELECT total_play, total_download from song where id_konten = \'{song_id}\'')
    records_song[0] = records_song[0] + cursor.fetchone()

    cursor.execute(
        f'SELECT album.judul from album, song where song.id_konten = \'{song_id}\' AND song.id_album = album.id')
    records_song[0] = records_song[0] + cursor.fetchone()

    cursor.execute(
        f'SELECT genre from genre where id_konten = \'{song_id}\'')
    records_genre = cursor.fetchall()

    cursor.execute(
        f'SELECT akun.nama from songwriter_write_song, songwriter, akun where songwriter_write_song.id_song = \'{song_id}\' AND songwriter.id = songwriter_write_song.id_songwriter AND songwriter.email_akun = akun.email')
    records_songwriter = cursor.fetchone()

    durasi = int(records_song[0][4]) * 60


    if request.method == 'POST':
        if 'download' in request.POST:
            # Handling the download button click
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                f'select total_download from song where id_konten = \'{song_id}\'')
            total = cursor.fetchall()
            total_download = total[0][0] + 1

            sudah = []
            cursor.execute(
                f'select id_song from downloaded_song where id_song = \'{song_id}\' AND email_downloader = \'{email}\'')
            sudah = cursor.fetchall()

            if len(sudah) > 0:
                return render(request, 'song_telah_download.html')
            
            cursor.execute(
                f'update song set total_download = \'{total_download}\' where id_konten = \'{song_id}\''
            )

            cursor.execute(
                f'insert into downloaded_song values( \'{song_id}\', \'{email}\' )'
            )

            connection.commit()
            url = reverse('playlist_player:pesan_download_song')
            url_param = f"{url}?song_id={song_id}"

            context = {
                'email': email,
            }
            return redirect(url_param, context)

    context = {
        'status': 'success',
        'records_song': records_song,
        'records_genre': records_genre,
        'records_songwriter': records_songwriter,
        'panjang': len(records_song),
        'song_id':song_id,
        'isPremium': isPremium,
        'durasi': durasi
    }
    return render(request, 'play_song.html', context)


def increment_play_count(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        song_id = data.get('song_id')

        if song_id:
            cursor.execute(f'select total_play from song where id_konten = \'{song_id}\'')
            total = cursor.fetchall()
            total_play = total[0][0] + 1

            cursor.execute(f'update song set total_play = \'{total_play}\' where id_konten = \'{song_id}\'')
            connection.commit()

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid song ID'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def add_song_to_user_playlist(request):
    song_id = request.GET.get('song_id')
    email = request.COOKIES.get('email')
    records_song = []
    list_playlist = []

    cursor.execute(
        f'SELECT id, judul from konten where id = \'{song_id}\'')
    records_song = cursor.fetchall()

    cursor.execute(
        f'SELECT akun.nama from akun, song, artist where song.id_konten = \'{song_id}\' AND song.id_artist = artist.id AND artist.email_akun = akun.email')
    records_song[0] = records_song[0] + cursor.fetchone()

    if request.method == 'POST' and not request.method == 'GET':
        playlist_id = request.POST.get('playlist_id')


        try:
            cursor.execute(
                f'select * from playlist_song where id_playlist = \'{playlist_id}\' AND id_song = \'{song_id}\''
            )
            ada = cursor.fetchone()
            if len(ada) > 0:
                return render(request, 'song_telah_ditambahkan.html')
            
            cursor.execute(
                "INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s)", [playlist_id, song_id]
            )
            connection.commit()
            url = reverse('playlist_player:pesan_add_song_to_playlist')
            url_with_params = f"{url}?song_id={song_id}"
            return redirect(url_with_params)
        
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Error: {e}", status=500)
            # return response
            # return render(request, 'add_song_to_user_playlist.html', context)



    cursor.execute(
        f'select id_playlist, judul from user_playlist where email_pembuat = \'{email}\''
    )
    list_playlist = cursor.fetchall()
    context = {
        'records_song': records_song,
        'list_playlist': list_playlist,

    }
    return render(request, 'add_song_to_user_playlist.html', context)

def pesan_add_song_to_playlist(request):
    song_id = request.GET.get('song_id')
    # playlist_id = request.GET.get('playlist_id')
    records = []
    cursor.execute(
        f'SELECT judul from konten where konten.id = \'{song_id}\'')
    records = cursor.fetchall()

    context = {
        'records': records,
        'song_id': song_id
    }
    return render(request, 'pesan_add_song_to_playlist.html', context)



def play_user_playlist(request): 
    playlist_id = request.GET.get('playlist_id')

    email = request.COOKIES.get('email')
    records_playlist = [] 
    records_song = []

    # Mengambil data playlist berdasarkan playlist_id
    cursor.execute(f'SELECT * FROM user_playlist WHERE id_playlist = \'{playlist_id}\'')
    records_playlist = cursor.fetchall()

    cursor.execute(f'SELECT id_song FROM playlist_song WHERE id_playlist = %s', [playlist_id])
    records_song = cursor.fetchall()
    for i in range(len(records_song)):
        cursor.execute( 
            f'SELECT konten.judul, akun.nama, konten.durasi, konten.id '
            f'FROM konten, song, artist, akun '
            f'WHERE konten.id = \'{records_song[i][0]}\' AND konten.id = song.id_konten '
            f'AND song.id_artist = artist.id AND artist.email_akun = akun.email')
        records_song[i] = records_song[i] + cursor.fetchone() 


    if request.method == 'POST':
        if 'shuffle_play' in request.POST:
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert ke tabel AKUN_PLAY_PLAYLIST 
            cursor.execute(
                f'INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu) '
                f'VALUES (\'{email}\', \'{records_playlist[0][1]}\', \'{records_playlist[0][0]}\', \'{current_timestamp}\')')

            connection.commit()
 
            # Insert ke tabel AKUN_PLAY_SONG untuk setiap lagu dalam playlist 
            test = 0
            for i in range((len(records_song)//2)-1):
                id = records_song[i][0] 
                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    f'INSERT INTO akun_play_song (email_pemain, id_song, waktu) '
                    f'VALUES (\'{email}\', \'{id}\', \'{current_timestamp}\')')
                test += 1
                if test > (len(records_song)//2):
                    break
   
            connection.commit()
            
            return redirect(reverse("playlist_player:play_user_playlist") + f'?playlist_id={playlist_id}')
        
        else: 
            for song in records_song:
                song_id = song[0]
                if f'play_song_{song_id}' in request.POST:
                    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(
                        f'INSERT INTO akun_play_song (email_pemain, id_song, waktu) '
                        f'VALUES (\'{email}\', \'{song_id}\', \'{current_timestamp}\')')

                    connection.commit()
                    url = reverse('playlist_player:play_song')
                    url_with_params = f"{url}?song_id={song_id}"
                    return redirect(url_with_params)

    # Konversi durasi total playlist ke format _ jam _ menit
    total_durasi_menit = records_playlist[0][7]
    total_jam = total_durasi_menit // 60
    total_menit = total_durasi_menit % 60
    total_durasi_format = f'{total_jam} jam {total_menit} menit'

    context = {
        'status': 'success',
        'records_playlist': records_playlist,
        'records_song': records_song,
        'playlist_id': playlist_id,
        'total_durasi_format': total_durasi_format
    }

    response = render(request, 'play_user_playlist.html', context)
    response.set_cookie('playlist_id', playlist_id)
    return response


def ubah_playlist(request):
    id_playlist = request.GET.get('id_playlist')

    # if not id_playlist:
    #     return redirect('playlist_player:user_playlist')  
  

    if request.method == 'POST':

        judul = request.POST['judul']
        deskripsi = request.POST['deskripsi']

        cursor.execute(
            f'update user_playlist set judul = \'{judul}\', deskripsi = \'{deskripsi}\' where  id_user_playlist = \'{id_playlist}\'')
        connection.commit()
        return redirect('playlist_player:user_playlist')
    
    judul_playlist = ''
    deskripsi_playlist = ''

    cursor.execute(
        """SELECT judul, deskripsi
            FROM user_playlist
            WHERE id_user_playlist = %s;
        """, [id_playlist]
    )
    result = cursor.fetchone()

    if result:
        judul_playlist, deskripsi_playlist = result

    return render(request, 'ubah_playlist.html', {
        'judul': judul_playlist,
        'deskripsi': deskripsi_playlist
    })  

def hapus_playlist(request):
    id_playlist = request.GET.get('id_playlist')
    cursor.execute(
        f'delete from user_playlist where id_user_playlist = \'{id_playlist}\''
    )
    cursor.execute(
        f'delete from playlist_song where id_user_playlist = \'{id_playlist}\''
    )
    connection.commit()
    return HttpResponseRedirect(reverse("playlist_player:user_playlist"))


def pesan_download_song(request):
    song_id = request.GET.get('song_id')
    records = []
    cursor.execute(
        f'SELECT judul from konten where konten.id = \'{song_id}\'')
    records = cursor.fetchall()

    context = {
        'records': records,
        'song_id': song_id
    }
    return render(request, 'pesan_download_song.html', context)

def hapus_song(request):
    id_song = request.GET.get('song_id')
    id_playlist = request.GET.get('playlist_id')
    cursor.execute(
        f'delete from playlist_song where id_song = \'{id_song}\' AND id_playlist = \'{id_playlist}\''
    )
    connection.commit()
    return HttpResponseRedirect(reverse("playlist_player:detail_playlist") + f'?playlist_id={id_playlist}')
