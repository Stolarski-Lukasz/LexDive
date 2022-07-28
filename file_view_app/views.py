from django.shortcuts import render

# Create your views here.

# diplaying interface
def index(request):
    return render(request, 'index.html')
