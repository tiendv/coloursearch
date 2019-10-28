from django.shortcuts import render


def about(request, *args,  **kwargs):
    print(request.user)
    return render(request, 'html/about.html', {})