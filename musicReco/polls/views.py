from django.shortcuts import render
from .services import search_artists
from .services import artist_top_tracks

# Create your views here.

def index(request):
    query = request.GET.get('search')
    artists = []  # services.py에서 정의한 함수 호출
    
    if query:
        artists = search_artists(query)
    
    return render(request, 'index.html', {'artists': artists})

def get_tracks(request):
    if request.method == 'POST':
        # 선택된 artist ID 가져오기
        artist_ids = request.POST.getlist('artist_ids[]')

        all_tracks = artist_top_tracks(artist_ids)

        return render(request, 'tracks.html', {'tracks':all_tracks})
        
    return JsonResponse({'error': 'Invalid Request'}, status=400)