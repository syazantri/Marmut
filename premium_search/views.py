from django.shortcuts import render

# Create your views here.
def cek_langganan(request):
    return render(request, 'cek_langganan.html')

def downloaded_song(request):
    return render(request, 'downloaded_song.html')

def search_bar(request):
    return render(request, 'search.html')

def not_found(request):
    return render(request, 'not_found.html')

def delete(request):
    return render(request, 'delete.html')

def payment(request):
    return render(request, 'payment.html')

def riwayat(request):
    return render(request, 'riwayat.html')