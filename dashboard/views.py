from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard_biasa.html')

def dashboard_label(request):
    return render(request, 'dashboard_label.html')

def dashboard_artist_songwriter(request):
    return render(request, 'dashboard_artist_songwriter.html')

def dashboard_podcaster(request):
    return render(request, 'dashboard_podcaster.html')