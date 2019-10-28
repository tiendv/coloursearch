from django.shortcuts import render


def home(request, *args, **kwargs):
    print(request.user)
    return render(request, 'html/home.html', {})