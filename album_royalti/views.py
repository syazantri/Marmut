import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import *
from datetime import datetime

def cek_royalti(request):
    role = request.COOKIES.get('role')
    isArtist = ""
    isSongwriter = ""
    records_royalti_label = []
    records_royalti_artist = []
    records_royalti_songwriter = []

    if role == "label":
        idPemilikCiptaLabel = request.COOKIES.get('idPemilikCiptaLabel')

        cursor.execute(
            f'select rate_royalti from pemilik_hak_cipta where id = \'{idPemilikCiptaLabel}\'')
        rate_royalti_label = cursor.fetchone()

        cursor.execute(
            f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaLabel}\'')
        records_royalti_label = cursor.fetchall()
        if len(records_royalti_label) != 0:
            for i in range(len(records_royalti_label)):
                cursor.execute(
                    f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_label[i][0]}\'')
                records_royalti_label[i] = records_royalti_label[i] + cursor.fetchone()

                cursor.execute(
                    f'''
                    UPDATE royalti
                    SET jumlah = {int(records_royalti_label[i][3])} * {int(rate_royalti_label[0])}
                    WHERE id_pemilik_hak_cipta = \'{idPemilikCiptaLabel}\' AND id_song = \'{records_royalti_label[i][0]}\'
                    '''
                )

                cursor.execute(
                    f'select judul from album where id = \'{records_royalti_label[i][2]}\'')
                records_royalti_label[i] = records_royalti_label[i] + cursor.fetchone()
                cursor.execute(
                    f'select judul from konten where id = \'{records_royalti_label[i][0]}\'')
                records_royalti_label[i] = records_royalti_label[i] + cursor.fetchone()

            for i in range(len(records_royalti_label)):
                cursor.execute(
                    f'select jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaLabel}\'')
                tuple_royalti_label = (int(records_royalti_label[i][3]) * int(rate_royalti_label[0]),)
                records_royalti_label[i] = records_royalti_label[i] + tuple_royalti_label

            connection.commit()
    else:
        isArtist = request.COOKIES.get('isArtist')
        isSongwriter = request.COOKIES.get('isSongwriter')

        if isArtist == "True" :
            idPemilikCiptaArtist = request.COOKIES.get('idPemilikCiptaArtist')
            cursor.execute(
                f'select rate_royalti from pemilik_hak_cipta where id = \'{idPemilikCiptaArtist}\'')
            rate_royalti_artist = cursor.fetchone()

            cursor.execute(
                f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaArtist}\'')
            records_royalti_artist = cursor.fetchall()
            if len(records_royalti_artist) != 0:
                for i in range(len(records_royalti_artist)):
                    cursor.execute(
                        f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_artist[i][0]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + cursor.fetchone()

                    cursor.execute(
                    f'''
                    UPDATE royalti
                    SET jumlah = {int(records_royalti_artist[i][3])} * {int(rate_royalti_artist[0])}
                    WHERE id_pemilik_hak_cipta = \'{idPemilikCiptaArtist}\' AND id_song = \'{records_royalti_artist[i][0]}\'
                    '''
                    )
                    
                    cursor.execute(
                        f'select judul from album where id = \'{records_royalti_artist[i][2]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + cursor.fetchone()
                    cursor.execute(
                        f'select judul from konten where id = \'{records_royalti_artist[i][0]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + cursor.fetchone()

                for i in range(len(records_royalti_artist)):
                    cursor.execute(
                        f'select jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaArtist}\'')
                    tuple_royalti_artist = (int(records_royalti_artist[i][3]) * int(rate_royalti_artist[0]),)
                    records_royalti_artist[i] = records_royalti_artist[i] + tuple_royalti_artist


        if isSongwriter == "True" :
            idPemilikCiptaSongwriter = request.COOKIES.get('idPemilikCiptaSongwriter')
            cursor.execute(
                f'select rate_royalti from pemilik_hak_cipta where id = \'{idPemilikCiptaSongwriter}\'')
            rate_royalti_songwriter = cursor.fetchone()

            cursor.execute(
                f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaSongwriter}\'')
            records_royalti_songwriter = cursor.fetchall()
            if len(records_royalti_songwriter) != 0:
                for i in range(len(records_royalti_songwriter)):
                    cursor.execute(
                        f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_songwriter[i][0]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + cursor.fetchone()

                    cursor.execute(
                    f'''
                    UPDATE royalti
                    SET jumlah = {int(records_royalti_songwriter[i][3])} * {int(rate_royalti_songwriter[0])}
                    WHERE id_pemilik_hak_cipta = \'{idPemilikCiptaSongwriter}\' AND id_song = \'{records_royalti_songwriter[i][0]}\'
                    '''
                    )

                    cursor.execute(
                        f'select judul from album where id = \'{records_royalti_songwriter[i][2]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + cursor.fetchone()
                    cursor.execute(
                        f'select judul from konten where id = \'{records_royalti_songwriter[i][0]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + cursor.fetchone()

                for i in range(len(records_royalti_songwriter)):
                    cursor.execute(
                        f'select jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaSongwriter}\'')
                    tuple_royalti_songwriter = (int(records_royalti_songwriter[i][3]) * int(rate_royalti_songwriter[0]),)
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + tuple_royalti_songwriter

        connection.commit()

    context = {
        'status': 'success',
        'role': role,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'records_royalti_label': records_royalti_label,
        'records_royalti_artist': records_royalti_artist,
        'records_royalti_songwriter': records_royalti_songwriter,
    }
    response = render(request, 'cek_royalti.html', context)
    return response


def create_album(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    idArtist = request.COOKIES.get('idArtist')
    idSongwriter = request.COOKIES.get('idSongwriter')
    nama_artist = ""
    nama_songwriter = ""

    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('judul')
        label = request.POST.get('label')
        id_album = str(uuid.uuid4())
        cursor.execute(
            f'insert into album values (\'{id_album}\', \'{judul}\', 0, \'{label}\', 0)')
    
        judul_lagu = request.POST.get('judul_lagu')
        id_song = str(uuid.uuid4())
        durasi = request.POST.get('durasi')
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year
        year_now = '{:04d}'.format(current_year)
        songwriters = request.POST.getlist('songwriter[]')
        genres = request.POST.getlist('genre[]')

        if isArtist == "True":
            id_artist = idArtist
            id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
        else:
            id_artist = request.POST.get('artist')
            cursor.execute(
                f'select id_pemilik_hak_cipta from artist where id = \'{id_artist}\'')
            id_pemilik_hak_cipta_artist = cursor.fetchone()

        if isSongwriter == "True":
            songwriters.append(idSongwriter)

        # insert ke tabel konten
        cursor.execute(
            f'insert into konten values (\'{id_song}\', \'{judul_lagu}\', \'{date_now}\', \'{year_now}\', \'{durasi}\')')
        
        # insert ke tabel song
        cursor.execute(
            f'insert into song values (\'{id_song}\', \'{id_artist}\', \'{id_album}\', 0, 0)')
        
        # insert ke songwriter_write_song dan royalti
        for songwriter in songwriters:
            cursor.execute(
                f'select id_pemilik_hak_cipta from songwriter where id = \'{songwriter}\'')
            id_pemilik_hak_cipta_songwriter = cursor.fetchone();
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_songwriter[0]}\', \'{id_song}\', 0)')
            cursor.execute(
                f'insert into songwriter_write_song values (\'{songwriter}\', \'{id_song}\')')

        # insert ke genre
        for genre in genres:
            cursor.execute(
                f'insert into genre values (\'{id_song}\', \'{genre}\')')
        
        # insert royalti artist
        if isArtist == "True":
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_artist}\', \'{id_song}\', 0)')
        else:
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_artist[0]}\', \'{id_song}\', 0)')
        
        # insert royalti label
        cursor.execute(
            f'select id_label from album where id = \'{id_album}\'')
        id_label = cursor.fetchone()
        cursor.execute(
            f'select id_pemilik_hak_cipta from label where id = \'{id_label[0]}\'')
        id_pemilik_hak_cipta_label = cursor.fetchone()
        cursor.execute(
            f'insert into royalti values (\'{id_pemilik_hak_cipta_label[0]}\', \'{id_song}\', 0)')
        
        connection.commit()
        return redirect('album_royalti:list_edit_album')

    # untuk pilihan dropdown artist
    cursor.execute(
        f'select id, email_akun, id_pemilik_hak_cipta from artist')
    records_artist = cursor.fetchall()
    for i in range(len(records_artist)):
        cursor.execute(
            f'select nama from akun where email = \'{records_artist[i][1]}\'')
        records_artist[i] = records_artist[i] + cursor.fetchone()

    # untuk pilihan dropdown songwriter
    cursor.execute(
        f'select id, email_akun, id_pemilik_hak_cipta from songwriter')
    records_songwriter = cursor.fetchall()
    for i in range(len(records_songwriter)):
        cursor.execute(
            f'select nama from akun where email = \'{records_songwriter[i][1]}\'')
        records_songwriter[i] = records_songwriter[i] + cursor.fetchone()

    # untuk pilihan dropdown genre
    cursor.execute(
        f'select distinct genre from genre')
    records_genre = cursor.fetchall()

    # get nama artist
    if isArtist == "True":
        cursor.execute(
            f'select email_akun from artist where id = \'{idArtist}\'')
        email_artist = cursor.fetchone()
        cursor.execute(
            f'select nama from akun where email = \'{email_artist[0]}\'')
        nama_artist = cursor.fetchone()

    # get nama songwriter
    if isSongwriter == "True":
        cursor.execute(
            f'select email_akun from songwriter where id = \'{idSongwriter}\'')
        email_songwriter = cursor.fetchone()
        cursor.execute(
            f'select nama from akun where email = \'{email_songwriter[0]}\'')
        nama_songwriter = cursor.fetchone()

    # get nama label
    cursor.execute(
        f'select id, nama from label')
    list_label = cursor.fetchall()

    context = {
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'idArtist': idArtist,
        'idSongwriter': idSongwriter,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'nama_artist': nama_artist,
        'nama_songwriter': nama_songwriter,
        'list_label': list_label
    }
    return render(request, 'create_album.html', context)


def create_song(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    idArtist = request.COOKIES.get('idArtist')
    idSongwriter = request.COOKIES.get('idSongwriter')
    album_id = request.GET.get('album_id')
    nama_artist = ""
    nama_songwriter = ""

    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('judul')
        id_song = str(uuid.uuid4())
        durasi = request.POST.get('durasi')
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year
        year_now = '{:04d}'.format(current_year)
        songwriters = request.POST.getlist('songwriter[]')
        genres = request.POST.getlist('genre[]')

        if isArtist == "True":
            id_artist = idArtist
            id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
        else:
            id_artist = request.POST.get('artist')
            cursor.execute(
                f'select id_pemilik_hak_cipta from artist where id = \'{id_artist}\'')
            id_pemilik_hak_cipta_artist = cursor.fetchone()

        if isSongwriter == "True":
            songwriters.append(idSongwriter)

        # insert ke tabel konten
        cursor.execute(
            f'insert into konten values (\'{id_song}\', \'{judul}\', \'{date_now}\', \'{year_now}\', \'{durasi}\')')
        
        # insert ke tabel song
        cursor.execute(
            f'insert into song values (\'{id_song}\', \'{id_artist}\', \'{album_id}\', 0, 0)')
        
        # insert ke songwriter_write_song dan royalti
        for songwriter in songwriters:
            cursor.execute(
                f'select id_pemilik_hak_cipta from songwriter where id = \'{songwriter}\'')
            id_pemilik_hak_cipta_songwriter = cursor.fetchone()
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_songwriter[0]}\', \'{id_song}\', 0)')
            cursor.execute(
                f'insert into songwriter_write_song values (\'{songwriter}\', \'{id_song}\')')

        # insert ke genre
        for genre in genres:
            cursor.execute(
                f'insert into genre values (\'{id_song}\', \'{genre}\')')
        
        # insert royalti artist
        if isArtist == "True":
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_artist}\', \'{id_song}\', 0)')
        else:
            cursor.execute(
                f'insert into royalti values (\'{id_pemilik_hak_cipta_artist[0]}\', \'{id_song}\', 0)')
        
        # insert royalti label
        cursor.execute(
            f'select id_label from album where id = \'{album_id}\'')
        id_label = cursor.fetchone()
        cursor.execute(
            f'select id_pemilik_hak_cipta from label where id = \'{id_label[0]}\'')
        id_pemilik_hak_cipta_label = cursor.fetchone()
        cursor.execute(
            f'insert into royalti values (\'{id_pemilik_hak_cipta_label[0]}\', \'{id_song}\', 0)')
        
        # update album
        # cursor.execute(
        #     f'select jumlah_lagu, total_durasi from album where id = \'{album_id}\'')
        # album_saat_ini = cursor.fetchone()
        # new_total_durasi = int(album_saat_ini[1]) + int(durasi)
        # new_jumlah_lagu = int(album_saat_ini[0]) + 1
        # cursor.execute(
        #     f'UPDATE album SET jumlah_lagu = {new_jumlah_lagu}, total_durasi = {new_total_durasi} WHERE id = \'{album_id}\'')
        
        connection.commit()
        return redirect('album_royalti:list_edit_album')

    # untuk pilihan dropdown artist
    cursor.execute(
        f'select id, email_akun, id_pemilik_hak_cipta from artist')
    records_artist = cursor.fetchall()
    for i in range(len(records_artist)):
        cursor.execute(
            f'select nama from akun where email = \'{records_artist[i][1]}\'')
        records_artist[i] = records_artist[i] + cursor.fetchone()

    # untuk pilihan dropdown songwriter
    cursor.execute(
        f'select id, email_akun, id_pemilik_hak_cipta from songwriter')
    records_songwriter = cursor.fetchall()
    for i in range(len(records_songwriter)):
        cursor.execute(
            f'select nama from akun where email = \'{records_songwriter[i][1]}\'')
        records_songwriter[i] = records_songwriter[i] + cursor.fetchone()

    # untuk pilihan dropdown genre
    cursor.execute(
        f'select distinct genre from genre')
    records_genre = cursor.fetchall()

    # get nama album
    cursor.execute(
        f'select judul from album where id = \'{album_id}\'')
    judul_album = cursor.fetchone()

    # get nama artist
    if isArtist == "True":
        cursor.execute(
            f'select email_akun from artist where id = \'{idArtist}\'')
        email_artist = cursor.fetchone()
        cursor.execute(
            f'select nama from akun where email = \'{email_artist[0]}\'')
        nama_artist = cursor.fetchone()

    # get nama songwriter
    if isSongwriter == "True":
        cursor.execute(
            f'select email_akun from songwriter where id = \'{idSongwriter}\'')
        email_songwriter = cursor.fetchone()
        cursor.execute(
            f'select nama from akun where email = \'{email_songwriter[0]}\'')
        nama_songwriter = cursor.fetchone()

    context = {
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'idArtist': idArtist,
        'idSongwriter': idSongwriter,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'judul_album': judul_album,
        'nama_artist': nama_artist,
        'nama_songwriter': nama_songwriter,
    }
    return render(request, 'create_song.html', context)


def list_album(request):
    email = request.COOKIES.get('email')

    cursor.execute(
        f'select * from label where email = \'{email}\'')
    label = cursor.fetchmany()
    if len(label) == 1:
        # Cari album yang dimiliki label
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
        response = render(request, 'list_album.html', context)
        response.set_cookie('role', 'label')
        response.set_cookie('email', email)
        response.set_cookie('id', label[0][0])
        response.set_cookie('idPemilikCiptaLabel', label[0][5])
        return response
    return render(request, 'list_album.html')


def list_edit_album(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    records_album_artist = []
    records_album_songwriter = []
    artistHasAlbum = False
    songwriterHasAlbum = False

    # kalau dia artist, list album dia sebagai artist
    if isArtist == "True" :
        id_artist = request.COOKIES.get('idArtist')
        list_album_id_artist = []
        cursor.execute(
            f'SELECT DISTINCT id_album FROM SONG WHERE id_artist = \'{id_artist}\'')
        list_album_id_artist = cursor.fetchall()

        if len(list_album_id_artist) != 0:
            artistHasAlbum = True
            for id_album in list_album_id_artist:
                cursor.execute(
                    f'SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album[0]}\'')
                records_album_artist.append(cursor.fetchone())
            for i in range(len(records_album_artist)):
                cursor.execute(
                    f'SELECT nama FROM LABEL WHERE id = \'{records_album_artist[i][2]}\'')
                records_album_artist[i] = records_album_artist[i] + cursor.fetchone() 

    # kalau dia songwriter, list album dia sebagai songwriter
    if isSongwriter == "True":
        id_songwriter = request.COOKIES.get('idSongwriter')
        list_song_id_songwriter = []
        cursor.execute(
            f'SELECT id_song FROM songwriter_write_song WHERE id_songwriter =  \'{id_songwriter}\'')
        list_song_id_songwriter = cursor.fetchall()

        if len(list_song_id_songwriter) != 0:
            list_album_id_songwriter = []
            for song in list_song_id_songwriter:
                cursor.execute(
                    f'SELECT DISTINCT id_album FROM SONG WHERE id_konten = \'{song[0]}\'')
                album_id_sekarang = cursor.fetchone()
                if album_id_sekarang not in list_album_id_songwriter:
                    list_album_id_songwriter.append(album_id_sekarang)

            if len(list_album_id_songwriter) != 0:
                songwriterHasAlbum = True
                for id_album in list_album_id_songwriter:
                    cursor.execute(
                        f'SELECT id, judul, id_label, jumlah_lagu, total_durasi from album where id = \'{id_album[0]}\'')
                    records_album_songwriter.append(cursor.fetchone())
                for i in range(len(records_album_songwriter)):
                    cursor.execute(
                        f'SELECT nama FROM LABEL WHERE id = \'{records_album_songwriter[i][2]}\'')
                    records_album_songwriter[i] = records_album_songwriter[i] + cursor.fetchone() 
        
    context = {
        'status': 'success',
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'artistHasAlbum': artistHasAlbum,
        'songwriterHasAlbum': songwriterHasAlbum,
        'records_album_artist': records_album_artist,
        'records_album_songwriter': records_album_songwriter,
    }
    response = render(request, 'list_edit_album.html', context)
    return response


def list_song(request):
    album_id = request.GET.get('album_id')
    records_song = []

    cursor.execute(
        f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    records_song = cursor.fetchall()
    for i in range(len(records_song)):
        cursor.execute(
            f'SELECT judul, tanggal_rilis, tahun, durasi from konten where id = \'{records_song[i][0]}\'')
        records_song[i] = records_song[i] + cursor.fetchone()
    cursor.execute(
        f'SELECT judul from album where id = \'{album_id}\'')
    judul_album = cursor.fetchone()[0]

    context = {
        'status': 'success',
        'records_song': records_song,
        'album_id': album_id,
        'judul_album': judul_album
    }
    response = render(request, 'list_song.html', context)
    return response

def delete_song(request):
    id_song = request.GET.get('song_id')
    album_id = request.GET.get('album_id')
    
    cursor.execute(
        f'delete from song where id_konten = \'{id_song}\'')
    cursor.execute(
        f'delete from konten where id = \'{id_song}\'')
    
    connection.commit()
    return HttpResponseRedirect(reverse('album_royalti:list_song') + f'?album_id={album_id}')

def delete_album(request):
    album_id = request.GET.get('album_id')
    role = request.COOKIES.get('role')
    records_song = []

    cursor.execute(
        f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    records_song = cursor.fetchall()
    for record in records_song:
        cursor.execute(
            f'delete from song where id_konten = \'{record[0]}\'')
        cursor.execute(
            f'delete from konten where id = \'{record[0]}\'')
    cursor.execute(
        f'delete from album where id = \'{album_id}\'')
    
    connection.commit()
    if role == "pengguna":
        return HttpResponseRedirect(reverse('album_royalti:list_edit_album'))
    else:
        return HttpResponseRedirect(reverse('dashboard:list_album'))