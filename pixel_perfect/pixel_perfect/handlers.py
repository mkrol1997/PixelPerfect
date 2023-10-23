from django.shortcuts import render


def Custom404Handler(request, exception):
    return render(request, 'pixel_perfect/404.html')


def Custom500Handler(request):
    return render(request, 'pixel_perfect/500.html')