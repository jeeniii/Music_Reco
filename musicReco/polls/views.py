import json
from django.shortcuts import render
from django.http import JsonResponse
from .services import search_artists, artist_top_tracks, recommendations

# Create your views here.

def index(request):
    query = request.GET.get('search','')
    artists = []  # services.py에서 정의한 함수 호출
    
    if query:
        artists = search_artists(query)
    
    return render(request, 'index.html', {'artists': artists, 'query': query})

def get_tracks(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 선택된 artist ID 가져오기
        artist_ids = body.get('artist_ids',[])
        all_tracks = artist_top_tracks(artist_ids)

        return JsonResponse({'tracks': all_tracks})
        
    return JsonResponse({'error': 'Invalid Request'}, status=400)

def recommend_tracks(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 선택된 tracks ID 가져오기
        track_ids = body.get('track_ids',[])
        recommend_all_tracks = recommendations(track_ids)

        return JsonResponse({'recommend_all_tracks': recommend_all_tracks})
    
    return JsonResponse({'error': 'Invalid Request'}, status=400)