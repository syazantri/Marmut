from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
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
            with connection.cursor() as cursor:
                cursor.execute("SET SEARCH_PATH TO A5")
                cursor.execute("SELECT COUNT(*) FROM TRANSACTION WHERE email = %s AND timestamp_berakhir > CURRENT_TIMESTAMP", [email])
                active_subscription_count = cursor.fetchone()[0]
                
                if active_subscription_count > 0:
                    return HttpResponse("Error: User already has an active subscription.", status=400)
            
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
                # Insert into TRANSACTION table
                cursor.execute("""
                    INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, [transaction_id, jenis_paket, email, start_date, end_date, metode_bayar, harga])

                # Check if the user is in the PREMIUM table
                cursor.execute("SELECT COUNT(*) FROM PREMIUM WHERE email = %s", [email])
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO PREMIUM (email) VALUES (%s);", [email])
                    
                    # Delete the user from NONPREMIUM table
                    cursor.execute("DELETE FROM NONPREMIUM WHERE email = %s;", [email])
                    
            return redirect('dashboard:dashboard')

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Error: {e}", status=500)
    
    return HttpResponse("Invalid request.", status=400)

def downloaded_song(request):
    email = request.COOKIES.get('email')
    if not email:
        return HttpResponse("Error: No email found in cookies.", status=400)

    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO A5")
        cursor.execute("""
            SELECT k.judul, ak.nama
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
                'judul': row[0],
                'nama_artist': row[1],
            }
            for row in rows
        ]

    return render(request, 'downloaded_song.html', {'songs': songs})

def delete(request, id_song):
    email = request.COOKIES.get('email')
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
    return render(request, 'search.html')

def not_found(request):
    return render(request, 'not_found.html')