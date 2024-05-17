import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime

# Create your views here.
def play_podcast(request):
    return render(request, 'play_podcast.html')

def create_podcast(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        id_podcast = str(uuid.uuid4())
        genres = request.POST.getlist('genre[]')
        email_podcaster = request.COOKIES.get('email')

        # Insert ke tabel konten
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year

        # untuk pilihan dropdown genre
        cursor.execute(
            f'select distinct genre from genre')
        records_genre = cursor.fetchall()

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

    # # untuk pilihan dropdown genre
    # cursor.execute(
    #     f'select distinct genre from genre')
    # records_genre = cursor.fetchall()

    context = {
        'records_genre': records_genre,
    }

    return render(request, 'create_podcast.html', context)


def lihat_chart(request):
    return render(request, 'lihat_chart.html')

def detail_chart(request):
    return render(request, 'detail_chart.html')

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


def create_episode(request, podcast_id):
    if request.method == 'POST':
        # Mendapatkan data yang dikirimkan melalui form
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        durasi = request.POST.get('durasi')
        id_episode = uuid.uuid4()
        date_now = datetime.date.today()

        # Insert data episode ke dalam database
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO episode (
                    id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, [id_episode, podcast_id, judul, deskripsi, durasi, date_now])
        connection.commit()
        # Redirect ke halaman list episode setelah membuat episode
        return redirect('podcast_chart:list_episode', podcast_id=podcast_id)

    else:
        # Mengambil informasi podcast yang dipilih
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT judul FROM konten WHERE id = %s', (podcast_id,)
            )
            podcast_title = cursor.fetchone()[0]

        context = {
            'podcast_title': podcast_title,
        }

        return render(request, 'create_episode.html', context)


def list_episode(request, podcast_id):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT konten.id, konten.judul 
                FROM konten
                JOIN podcast ON konten.id = podcast.id_konten
                WHERE podcast.id_konten = %s """,[podcast_id])
        podcast = cursor.fetchone()
        cursor.execute("""
                SELECT judul, deskripsi, durasi, tanggal_rilis, episode.id_episode
                FROM episode 
                WHERE id_konten_podcast = %s;
                """, [podcast_id])
        episodes = cursor.fetchall()
    connection.commit()

    context = {
            'podcast' : {
                'id':podcast[0],
                'judul': podcast[1]}, 
                'episodes': [
                    {
                        'title': row[0], 
                        'description': row[1], 
                        'duration': f"{row[2]} menit", 
                        'date': row[3].strftime('%Y-%m-%d'), 
                        'episode_id':row[4]
                    } for row in episodes
                ]
            }
        
    
    return render(request, 'list_episode.html', context)