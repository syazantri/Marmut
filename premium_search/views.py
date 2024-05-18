from django.shortcuts import render, redirect
from django.db import connection
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse

def riwayat(request):
    email = request.COOKIES.get('email') 
    if not email:
        return HttpResponse("Error: No email found in cookies.", status=400)

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SET SEARCH_PATH TO A5")
            cursor.execute("SELECT * FROM TRANSACTION WHERE email = %s;", [email])
            rows = cursor.fetchall()
            transactions = [
                {
                    'id': row[0],
                    'jenis_paket': row[1],
                    'email': row[2],
                    'timestamp_dimulai': row[3],
                    'timestamp_berakhir': row[4],
                    'metode_bayar': row[5],
                    'nominal': row[6]
                }
                for row in rows
            ]
        return render(request, 'riwayat.html', {'transactions': transactions})

def cek_langganan(request):
    if request.method == 'POST':
        data = request.POST
        email = request.COOKIES.get('email') 
        jenis_paket = data.get('jenis_paket')
        metode_bayar = data.get('metode_bayar')
        
        package_durations = {
            '1 bulan': 1,
            '3 bulan': 3,
            '6 bulan': 6,
            '1 tahun': 12
        }

        duration = package_durations[jenis_paket]
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration * 30) 
        transaction_id = str(uuid.uuid4())

        with connection.cursor() as cursor:
            cursor.execute("SELECT harga FROM PAKET WHERE jenis = %s;", [jenis_paket])
            result = cursor.fetchone()
            if result:
                nominal = result[0]
            else:
                return render(request, 'cek_langganan.html', {'error': 'Package type not found'})

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, [transaction_id, jenis_paket, email, start_date, end_date, metode_bayar, nominal])
            

            cursor.execute("SELECT * FROM PREMIUM WHERE email = %s;", [email])
            result = cursor.fetchone()
            
            if not result:
                cursor.execute("INSERT INTO PREMIUM (email) VALUES (%s);", [email])
                cursor.execute("DELETE FROM NONPREMIUM WHERE email = %s;", [email])
                cursor.commit()
        
    return render(request, 'cek_langganan.html')


def payment(request):
    jenis_paket = request.GET.get('jenis_paket')
    harga = request.GET.get('harga')
    return render(request, 'payment.html', {'jenis_paket': jenis_paket, 'harga': harga})

def process_payment(request):
    if request.method == 'POST':
        email = request.COOKIES.get('email')  
        jenis_paket = request.POST.get('jenis_paket').strip()
        harga = request.POST.get('harga').strip()
        metode_bayar = request.POST.get('metode_bayar').strip()

        if not email:
            return HttpResponse("Error: No email found in cookies.", status=400)
        
        try:
            
            package_durations = {
                '1 bulan': 1,
                '3 bulan': 3,
                '6 bulan': 6,
                '1 tahun': 12
            }

            if jenis_paket not in package_durations:
                return HttpResponse("Error: Invalid package type.", status=400)

            duration = package_durations[jenis_paket]
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration * 30)

            transaction_id = str(uuid.uuid4())

            with connection.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO A5")
                # Insert into TRANSACTION table
                cursor.execute("""
                    INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, [transaction_id, jenis_paket, email, start_date, end_date, metode_bayar, harga])

                # Check if the user is in the PREMIUM table
                cursor.execute("SELECT 1 FROM PREMIUM WHERE email = %s", [email])
                found = cursor.fetchone()
                print(found[0])
                print(email)
                
                if not found[0]:
                    cursor.execute("DELETE FROM NONPREMIUM WHERE email = %s;", [email])
                    cursor.execute("INSERT INTO PREMIUM (email) VALUES (%s);", [email])

                    # Delete the user from NONPREMIUM table
                    
                connection.commit()
                    
                    
            return redirect('dashboard:dashboard')

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'already_subscribed.html')
            
    
    return HttpResponse("Invalid request.", status=400)

def downloaded_song(request):
    email = request.COOKIES.get('email')
    if not email:
        return HttpResponse("Error: No email found in cookies.", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO A5")
        cursor.execute("""
            SELECT k.judul, ak.nama, ds.id_song
            FROM DOWNLOADED_SONG ds
            JOIN SONG s ON ds.id_song = s.id_konten
            JOIN KONTEN k ON s.id_konten = k.id
            JOIN ARTIST a ON s.id_artist = a.id
            JOIN AKUN ak ON a.email_akun = ak.email
            WHERE ds.email_downloader = %s
        """, [email])
        rows = cursor.fetchall()
        songs = [
            {
                'id_song': row[2],
                'judul': row[0],
                'nama_artist': row[1],
            }
            for row in rows
        ]

    return render(request, 'downloaded_song.html', {'songs': songs})

def delete(request):
    email = request.COOKIES.get('email')
    id_song = request.GET.get('id_song')

    if not email:
        return HttpResponse("Error: No email found in cookies.", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO A5")
        cursor.execute("""
            DELETE FROM DOWNLOADED_SONG
            WHERE id_song = %s AND email_downloader = %s
        """, [id_song, email])

    return JsonResponse({'message': 'Song deleted successfully', 'id_song': id_song})


def search_bar(request):
    query = request.GET.get('query', '').lower()  # Get the query and convert it to lowercase
    if query:
        results = []
        with connection.cursor() as cursor:

            cursor.execute("SET SEARCH_PATH TO A5")
            # Searching in Podcasts
            cursor.execute("""
                SELECT 'PODCAST' AS type,
                k.judul AS judul,
                a.nama AS oleh,
                k.id AS id
                FROM podcast p
                JOIN konten k ON p.id_konten = k.id
                JOIN podcaster pod ON p.email_podcaster = pod.email
                JOIN akun a ON pod.email = a.email
                WHERE LOWER(k.judul) LIKE %s
            """, [f"%{query}%"])
            results.extend(cursor.fetchall())

            # Searching in Songs
            cursor.execute("""
                SELECT 'SONG' AS type,
                k.judul AS judul,
                a.nama AS oleh,
                k.id AS id
                FROM song s
                JOIN konten k ON s.id_konten = k.id
                JOIN artist ar ON s.id_artist = ar.id
                JOIN akun a ON ar.email_akun = a.email
                WHERE LOWER(k.judul) LIKE %s
            """, [f"%{query}%"])
            results.extend(cursor.fetchall())

            # Searching in User Playlists
            cursor.execute("""
                SELECT 'USER PLAYLIST' AS type,
                up.judul AS judul,
                a.nama AS oleh,
                up.id_user_playlist  AS id       
                FROM user_playlist up
                JOIN akun a ON up.email_pembuat = a.email
                WHERE LOWER(up.judul) LIKE %s
            """, [f"%{query}%"])
            results.extend(cursor.fetchall())

        context = {
            'query': query,
            'results': [{
                'type': result[0],
                'title': result[1],
                'by': result[2],
                'id' : result[3],
            } for result in results]
        }
        return render(request, 'search.html', context)