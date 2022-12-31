from django.shortcuts import render


# diplaying interface
def index(request):
    return render(request, 'index.html')
