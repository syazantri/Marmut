from django.shortcuts import render

def cek_royalti(request):
    return render(request, 'cek_royalti.html')

def create_album(request):
    return render(request, 'create_album.html')

def create_song(request):
    return render(request, 'create_song.html')

def list_album(request):
    return render(request, 'list_album.html')

def list_edit_album(request):
    return render(request, 'list_edit_album.html')

def list_song(request):
    return render(request, 'list_song.html')