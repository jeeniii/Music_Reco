import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_artists(artist_name, limit=10):
    artists_data = []
    search_artist = sp.search(artist_name, limit=limit, type='artist', market='KR')
    
    for artist in search_artist['artists']['items']:
        artist_data = {
            'name': artist['name'],
            'id': artist['id'],
            'image_url': artist['images'][-1]['url'] if artist['images'] else '',  # 이미지가 없는 경우 예외 처리
        }
        artists_data.append(artist_data)
    return artists_data

def artist_top_tracks(artist_ids):
    artist_tracks = {}
    for artist_id in artist_ids:
        artist_top_tracks = sp.artist_top_tracks(artist_id, country='KR')
        
        tracks = []
        for top_track in artist_top_tracks['tracks']:
            top_track_data = {
                'name': top_track['name'],
                'id': top_track['id'],
                'image_url': top_track['album']['images'][-1]['url'] if top_track['album']['images'] else '',
                'popularity': top_track['popularity']
            }
            tracks.append(top_track_data)
        # dictionary[key] = value
        artist_tracks[artist_id] = tracks
    return artist_tracks

