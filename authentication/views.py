from django.shortcuts import redirect, render
from authentication.forms import RegisterFormPengguna, RegisterFormLabel
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.query import *
import random
import uuid
import re

def main_auth(request):
    return render(request, 'main_auth.html')

# ------------------------ MULAI BENAR --------------------------------
# def show_main(request):
#     if request.COOKIES.get('role'):
        
def main_register(request):
    return render(request, 'main_register.html')

def register_pengguna(request):
    if request.method == 'POST' and not request.method == 'GET':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')
        role = request.POST.getlist('role')
        
        # check email is valid or not
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, email):
            form = RegisterFormPengguna(request.POST or None)
            context = {
                'form': form,
                'message': 'Email tidak valid',
            }
            return render(request, 'register_biasa.html', context)

        # if data is not complete
        if not email or not password or not nama or not gender or not tempat_lahir or not tanggal_lahir or not kota_asal:
            form = RegisterFormPengguna(request.POST or None)
            context = {
                'form': form,
                'message': 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu',
            }
            return render(request, 'register_biasa.html', context)

        # check email is already registered or not
        cursor.execute(f'select * from akun where email = \'{email}\'')
        records = cursor.fetchmany()
        if len(records) > 0:
            form = RegisterFormPengguna(request.POST or None)
            context = {
                'form': form,
                'message': 'Email sudah terdaftar',
            }
            return render(request, 'register_biasa.html', context)
        
        # Mengecek badge verified user
        if len(role) == 0:
            is_verified = 'FALSE'
        else:
            is_verified = 'TRUE'

        # insert data to database
        try:
            cursor.execute(
                f'insert into akun values (\'{email}\', \'{password}\', \'{nama}\', \'{gender}\', \'{tempat_lahir}\', \'{tanggal_lahir}\', \'{is_verified}\', \'{kota_asal}\')')
            # cursor.execute(    tidak jadii karena sudah di trigger
            #     f'insert into nonpremium values (\'{email}\')')
            if('Artist' in role):
                id_artist = str(uuid.uuid4())
                id_pemilik_hak_cipta = str(uuid.uuid4())
                list_rate_royalti = [100,200,300,400,500,600,700,800,900,1000]
                rate_royalti = random.choice(list_rate_royalti)
                cursor.execute(
                    f'insert into pemilik_hak_cipta values (\'{id_pemilik_hak_cipta}\', \'{rate_royalti}\')')
                cursor.execute(
                    f'insert into artist values (\'{id_artist}\', \'{email}\', \'{id_pemilik_hak_cipta}\')')
            if('Podcaster' in role):
                cursor.execute(   
                    f'insert into podcaster values (\'{email}\')')
            if('Songwriter' in role):
                id_songwriter = str(uuid.uuid4())
                id_pemilik_hak_cipta = str(uuid.uuid4())
                list_rate_royalti = [100,200,300,400,500,600,700,800,900,1000]
                rate_royalti = random.choice(list_rate_royalti)
                cursor.execute(
                    f'insert into pemilik_hak_cipta values (\'{id_pemilik_hak_cipta}\', \'{rate_royalti}\')')
                cursor.execute(
                    f'insert into songwriter values (\'{id_songwriter}\', \'{email}\', \'{id_pemilik_hak_cipta}\')')

            connection.commit()

            # set cookie and redirect to dashboard
            # response = HttpResponseRedirect(reverse('authentication:show_main'))
            # if('Artist' in role):
            #     response.set_cookie('isArtist', True)
            #     response.set_cookie('idArtist', id_artist)
            # if('Podcaster' in role):
            #     response.set_cookie('isPodcaster', True)
            # if('Songwriter' in role):
            #     response.set_cookie('isSongwriter', True)
            #     response.set_cookie('idSongwriter', id_songwriter)
            # if(len(role) == 0):
            #     response.set_cookie('isVerified', False)
            # response.set_cookie('email', email)
            # response.set_cookie('isPremium', False)
            # return response
            return redirect('authentication:login')

        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            form = RegisterFormPengguna(request.POST or None)
            # err slice to get only error message
            err = str(err).split('CONTEXT')[0]
            context = {
                'message': err,
            }

            return render(request, 'register_biasa.html', context)

    else:
        form = RegisterFormPengguna(request.POST or None)

        context = {
            'form': form
        }

        return render(request, 'register_biasa.html', context)
    
def register_label(request):
    
    if request.method == 'POST' and not request.method == 'GET':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')
        
        # check email is valid or not
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, email):
            form = RegisterFormPengguna(request.POST or None)
            context = {
                'form': form,
                'message': 'Email tidak valid',
            }
            return render(request, 'register_label.html', context)

        # if data is not complete
        if not email or not password or not nama or not kontak:
            form = RegisterFormLabel(request.POST or None)
            context = {
                'form': form,
                'message': 'Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu',
            }
            return render(request, 'register_label.html', context)

        # check email is already registered or not
        # cursor.execute(f'select * from akun where email = \'{email}\'')
        # records = cursor.fetchmany()
        # if len(records) > 0:
        #     form = RegisterFormLabel(request.POST or None)
        #     context = {
        #         'form': form,
        #         'message': 'Email sudah terdaftar',
        #     }
        #     return render(request, 'register_label.html', context)

        # insert data to database
        try:
            id_label = str(uuid.uuid4())
            id_pemilik_hak_cipta = str(uuid.uuid4())
            list_rate_royalti = [100,200,300,400,500,600,700,800,900,1000]
            rate_royalti = random.choice(list_rate_royalti)
            cursor.execute(
                f'insert into pemilik_hak_cipta values (\'{id_pemilik_hak_cipta}\', \'{rate_royalti}\')')
            cursor.execute(
                f'insert into label values (\'{id_label}\', \'{nama}\', \'{email}\', \'{password}\', \'{kontak}\', \'{id_pemilik_hak_cipta}\')')

            connection.commit()

            # set cookie and redirect to dashboard
            # response = HttpResponseRedirect(reverse('authentication:show_main'))
            # response.set_cookie('isLabel', True)
            # response.set_cookie('email', email)
            # return response
            return redirect('authentication:login')

        except Exception as err:
            connection.rollback()
            print("Oops! An exception has occured:", err)
            print("Exception TYPE:", type(err))
            form = RegisterFormLabel(request.POST or None)
            # err slice to get only error message
            err = str(err).split('CONTEXT')[0]
            context = {
                'form': form,
                'message': err,
            }

            return render(request, 'register_label.html', context)

    else:
        form = RegisterFormLabel(request.POST or None)

        context = {
            'form': form
        }

        return render(request, 'register_label.html', context)
    
def login(request):
    # # if user is logged in, redirect to dashboard
    # if request.COOKIES.get('email'):
    #     return HttpResponseRedirect(reverse('authentication:show_main'))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        cursor.execute(
            f'select * from akun where email = \'{email}\'')
        user = cursor.fetchmany()

        if len(user) == 0:
            cursor.execute(
                f'select * from label where email = \'{email}\'')
            label = cursor.fetchmany()
            if len(label) == 1 and label[0][3] == password:
                #Cari album yang dimiliki label
                id_label = label[0][0]
                cursor.execute(
                    f'select * from album where id_label = \'{id_label}\'')
                records_album = cursor.fetchall()
                if records_album is None:
                    label_hasalbum = False
                else:
                    label_hasalbum = True
                context = {
                    'role': 'label',
                    'status': 'success',
                    'id': label[0][0],
                    'nama': label[0][1],
                    'email': label[0][2],
                    'kontak': label[0][4],
                    'id_pemilik_hak_cipta': label[0][5],
                    'hasAlbum': label_hasalbum,
                    'records_album': records_album,
                }
                response = render(request, 'dashboard_label.html', context)
                response.set_cookie('role', 'label')
                response.set_cookie('email', email)
                response.set_cookie('id', label[0][0])
                response.set_cookie('idPemilikCiptaLabel', label[0][5])
                return response
            
            else:
                context = {
                'message': 'Mohon cek kembali email dan password anda.',
                'status': 'error',
                'role': None,
            }
            return render(request, 'login.html', context)

        elif len(user) == 1 and user[0][1] == password: #kalau email sesuai, password benar:
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
                role_verified_list.append('Podcaster')
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
            response.set_cookie('role', 'pengguna')
            response.set_cookie('statusLangganan', status_langganan)
            response.set_cookie('isArtist', isArtist)
            response.set_cookie('isSongwriter', isSongwriter)
            response.set_cookie('isPodcaster', isPodcaster)
            response.set_cookie('email', email)
            response.set_cookie('idArtist', id_artist)
            response.set_cookie('idSongwriter', id_songwriter)
            response.set_cookie('idPemilikCiptaArtist', id_pemilik_hak_cipta_artist)
            response.set_cookie('idPemilikCiptaSongwriter', id_pemilik_hak_cipta_songwriter)
            return response
            
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    
    response = HttpResponseRedirect(reverse('dashboard:homepage'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response