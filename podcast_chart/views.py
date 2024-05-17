import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.query import *
from datetime import datetime

# Create your views here.
def play_podcast(request):
    podcast_id = request.GET.get('podcast_id')
    data_podcast = {}
    data_episode = []

    # Query to get podcast details
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT konten.judul, konten.tanggal_rilis, konten.tahun, AKUN.nama AS podcaster_name, SUM(episode.durasi) AS total_durasi
            FROM podcast
            JOIN podcaster ON podcast.email_podcaster = podcaster.email 
            JOIN AKUN ON podcaster.email = AKUN.email 
            JOIN konten ON podcast.id_konten = konten.id 
            JOIN episode ON podcast.id_konten = episode.id_konten_podcast
            WHERE podcast.id_konten = %s
            GROUP BY konten.judul, konten.tanggal_rilis, konten.tahun, AKUN.nama;
        """, [podcast_id])
        result = cursor.fetchone()
        if result:
            total_durasi = result[4]
            hours = total_durasi // 60
            minutes = total_durasi % 60
            formatted_duration = f"{hours} jam {minutes} menit" if hours > 0 else f"{minutes} menit"
            data_podcast = {
                'judul': result[0],
                'tanggal_rilis': result[1],
                'tahun': result[2],
                'podcaster': result[3],
                'total_durasi': formatted_duration
            }

    # Query to get genres
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT genre FROM genre WHERE id_konten = %s
        """, [podcast_id])
        result = cursor.fetchall()
        if result:
            data_podcast['genre'] = [row[0] for row in result]

    # Query to get episodes details
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT judul, deskripsi, durasi, tanggal_rilis
            FROM episode
            WHERE id_konten_podcast = %s
        """, [podcast_id])
        kumpulan_episode = cursor.fetchall()
        for episode in kumpulan_episode:
            duration_hours = episode[2] // 60
            duration_minutes = episode[2] % 60
            formatted_duration = f"{duration_hours} jam {duration_minutes} menit" if duration_hours else f"{duration_minutes} menit"

            data_episode.append({
                'title': episode[0],
                'description': episode[1],
                'duration': formatted_duration,
                'date': episode[3].strftime('%d/%m/%Y')
            })

    context = {
        'detail_podcast': data_podcast,
        'kumpulan_episode': data_episode
    }

    return render(request, 'play_podcast.html', context)

def create_podcast(request):
    records_genre = []
    
    if request.method == 'POST':
        judul = request.POST.get('judul')
        id_podcast = str(uuid.uuid4())
        genres = request.POST.getlist('genre[]')
        email_podcaster = request.COOKIES.get('email')

        # Insert ke tabel konten
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)',
                (id_podcast, judul, date_now, current_year, 1)  
            )

            cursor.execute(
                'INSERT INTO podcast (id_konten, email_podcaster) VALUES (%s, %s)',
                (id_podcast, email_podcaster)
            )

            # Insert ke genre
            for genre in genres:
                cursor.execute(
                    'INSERT INTO genre (id_konten, genre) VALUES (%s, %s)',
                    (id_podcast, genre)
                )

            connection.commit()
        return redirect('podcast_chart:list_podcast')  # Mengarahkan ke halaman daftar podcast

    # Untuk pilihan dropdown genre
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT genre FROM genre')
        records_genre = cursor.fetchall()
    
    context = {
        'records_genre': records_genre
    }

    return render(request, 'create_podcast.html', context)


def lihat_chart(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT tipe FROM chart")
        charts = cursor.fetchall()
    
    context = {
        'charts': [{'tipe': row[0]} for row in charts]
    }

    return render(request, 'lihat_chart.html', context)


def detail_chart(request):
    tipe_top = request.GET.get('tipe_top')
    with connection.cursor() as cursor:
        if tipe_top == "Daily Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", akun.nama AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM akun_play_song
                JOIN song ON akun_play_song.id_song = song.id_konten JOIN konten ON song.id_konten = konten.id JOIN artist ON song.id_artist = artist.id JOIN akun ON artist.email_akun = akun.email
                WHERE akun_play_song.waktu::date = CURRENT_DATE
                GROUP BY konten.id, konten.judul, akun.nama, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top == "Weekly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", akun.nama AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM akun_play_song
                JOIN song ON akun_play_song.id_song = song.id_konten JOIN konten ON song.id_konten = konten.id JOIN artist ON song.id_artist = artist.id JOIN akun ON artist.email_akun = akun.email
                WHERE akun_play_song.waktu >= date_trunc('week', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, akun.nama, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top== "Monthly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", akun.nama AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM akun_play_song
                JOIN song ON akun_play_song.id_song = song.id_konten JOIN konten ON song.id_konten = konten.id JOIN artist ON song.id_artist = artist.id JOIN akun ON artist.email_akun = akun.email
                WHERE akun_play_song.waktu >= date_trunc('month', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, akun.nama, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        elif tipe_top == "Yearly Top 20":
            cursor.execute("""
                SELECT konten.id, konten.judul AS "Judul Lagu", akun.nama AS "Oleh", konten.tanggal_rilis AS "Tanggal Rilis", COUNT(*) AS "Total Plays"
                FROM akun_play_song
                JOIN song ON akun_play_song.id_song = song.id_konten JOIN konten ON song.id_konten = konten.id JOIN artist ON song.id_artist = artist.id JOIN akun ON artist.email_akun = akun.email
                WHERE akun_play_song.waktu >= date_trunc('year', CURRENT_DATE)
                GROUP BY konten.id, konten.judul, akun.nama, konten.tanggal_rilis
                ORDER BY "Total Plays" DESC
                LIMIT 20;
            """)
        else:
            return render(request, '404.html')
        song_favorit = cursor.fetchall()
    context = {
        'judul' : tipe_top,
        'list_song' : [
            {
                'id_lagu': row[0], 
                'title': row[1], 
                'artist': row[2], 
                'release_date': row[3].strftime('%d/%m/%Y'), 
                'total_plays': row[4]} for row in song_favorit]
    }
    return render(request, 'detail_chart.html', context)

def list_podcast(request):
    email = request.COOKIES.get("email")
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT konten.id, konten.judul AS podcast_title, COALESCE(SUM(episode.durasi), 0) AS total_durasi, COUNT(episode.id_konten_podcast) AS jumlah_episode
            FROM podcast
            JOIN konten ON podcast.id_konten = konten.id
            LEFT JOIN episode ON podcast.id_konten = episode.id_konten_podcast
            WHERE podcast.email_podcaster = %s
            GROUP BY konten.id, konten.judul
        """, [email])
        
        result = cursor.fetchall()

    context = {
        'podcasts': [
            {'podcast_id':row[0],
             'judul': row[1],
             'jumlah_episode': row[3], 
             'total_durasi': f"{row[2]} menit"} for row in result
        ]
    
    }

    return render(request, 'list_podcast.html', context)


def create_episode(request):
    podcast_id = request.GET.get('podcast_id')
    if request.method == 'POST':
        # Mendapatkan data yang dikirimkan melalui form
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        durasi = request.POST.get('durasi')
        id_episode = uuid.uuid4()
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')

        # Insert data episode ke dalam database
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO episode (
                    id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, [id_episode, podcast_id, judul, deskripsi, durasi, date_now])
        connection.commit()
        # Redirect ke halaman list episode setelah membuat episode
        return HttpResponseRedirect(reverse('podcast_chart:list_episode') + f'?podcast_id={podcast_id}')

    else:
        # Mengambil informasi podcast yang dipilih
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT judul FROM konten WHERE id = %s', (podcast_id,)
            )
            podcast_title = cursor.fetchone()

        context = {
            'podcast_title': podcast_title,
        }

        return render(request, 'create_episode.html', context)


def list_episode(request):
    podcast_id = request.GET.get('podcast_id')
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT konten.id, konten.judul 
                FROM konten
                JOIN podcast ON konten.id = podcast.id_konten
                WHERE podcast.id_konten = %s """, [podcast_id])
        podcast = cursor.fetchone()
        cursor.execute("""
                SELECT judul, deskripsi, durasi, tanggal_rilis, episode.id_episode
                FROM episode 
                WHERE id_konten_podcast = %s;
                """, [podcast_id])
        episodes = cursor.fetchall()
    connection.commit()

    def format_duration(duration):
        if duration >= 60:
            hours = duration // 60
            minutes = duration % 60
            return f"{hours} jam {minutes} menit"
        else:
            return f"{duration} menit"

    context = {
        'podcast': {
            'id': podcast[0],
            'judul': podcast[1]
        },
        'episodes': [
            {
                'title': row[0],
                'description': row[1],
                'duration': format_duration(row[2]),
                'date': row[3].strftime('%Y-%m-%d'),
                'episode_id': row[4]
            } for row in episodes
        ]
    }

    return render(request, 'list_episode.html', context)


def delete_podcast(request):
    podcast_id = request.GET.get('podcast_id')
    
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM podcast WHERE id_konten = %s', [podcast_id]
        )
        cursor.execute(
            'DELETE FROM konten WHERE id = %s', [podcast_id]
        )
        connection.commit()
    
    return HttpResponseRedirect(reverse('podcast_chart:list_podcast'))


def delete_episode(request):
    episode_id = request.GET.get('episode_id')
    podcast_id = request.GET.get('podcast_id')
    
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM episode WHERE id_episode = %s', [episode_id]
        )
        connection.commit()
    
    return HttpResponseRedirect(reverse('podcast_chart:list_episode') + f'?podcast_id={podcast_id}')