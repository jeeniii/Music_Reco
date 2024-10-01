from django.shortcuts import render
from .services import search_artists

# Create your views here.

def index(request):
    query = request.GET.get('search')
    artists = []  # services.py에서 정의한 함수 호출
    
    if query:
        artists = search_artists(query)
    
    return render(request, 'index.html', {'artists': artists})