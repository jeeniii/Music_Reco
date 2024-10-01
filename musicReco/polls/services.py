import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '6b25f06078274ba5b42eb8308bf107ce'
client_secret = '10a43a425e5e4a229ce7ba63f60a0374'
client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_artists(artist_name, limit=10):
    search_artist = sp.search(artist_name, limit=limit, type='artist', market='KR')
    
    artists_data = []
    
    for artist in search_artist['artists']['items']:
        artist_data = {
            'name': artist['name'],
            'image_url': artist['images'][-1]['url'] if artist['images'] else '',  # 이미지가 없는 경우 예외 처리
        }
        artists_data.append(artist_data)
    
    return artists_data