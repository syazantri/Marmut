from django.shortcuts import render

# Create your views here.
def play_podcast(request):
    return render(request, 'play_podcast.html')

def create_podcast(request):
    return render(request, 'create_podcast.html')

def lihat_chart(request):
    return render(request, 'lihat_chart.html')

def detail_chart(request):
    return render(request, 'detail_chart.html')

def list_podcast(request):
    return render(request, 'list_podcast.html')

def create_episode(request):
    return render(request, 'create_episode.html')

def list_episode(request):
    return render(request, 'list_episode.html')