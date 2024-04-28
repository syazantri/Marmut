from django.shortcuts import render

# Create your views here.
def play_podcast(request):
    return render(request, 'play_podcast.html')

def play_user_playlist(request):
    return render(request, 'play_user_playlist.html')

def lihat_chart(request):
    return render(request, 'lihat_chart.html')

def detail_chart(request):
    return render(request, 'detail_chart.html')