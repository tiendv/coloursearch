from django.http import HttpResponse
from django.shortcuts import render
import os
# Create your views here.


def home_view(request, *args, **kwargs):
    print(request.user)
    return render(request, 'html/home.html', {})


def about(request, *args,  **kwargs):
    print(request.user)
    return render(request, 'html/about.html', {})


def extract_features(request, *args, **kwargs):
    if request.method == 'POST':
        folder_path = request.POST.get('folder_path')
        print(folder_path)
    return render(request, 'html/extract-features.html', {})