from django.shortcuts import render


def not_found(request):
    return render(request, "404-v2.html")
