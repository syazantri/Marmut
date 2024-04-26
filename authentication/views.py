from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def login(request):
    return render(request, 'login.html')

def register_label(request):
    return render(request, 'register_label.html')

def register(request):
    return render(request, 'register_biasa.html')

def main_register(request):
    return render(request, 'main_register.html')

def main_auth(request):
    return render(request, 'main_auth.html')