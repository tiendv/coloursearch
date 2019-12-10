from django.shortcuts import render


def homepage(request, *args, **kwargs):
    print(request.user)
    return render(request, 'html/homepage.html', {})