# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import pprint


# cid = '6b25f06078274ba5b42eb8308bf107ce' # Client ID
# secret = '10a43a425e5e4a229ce7ba63f60a0374' # Client Secret
# redirect_uri = 'http://localhost:8888/callback' # redirect uri
# sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = cid, client_secret = secret, redirect_uri = redirect_uri))

# result = sp.search('iu', limit = 3, type = 'artist')
# # pprint.pprint(result['artists']['items'][2])

# artistID = 'spotify:artist:3HqSLMAZ3g3d5poNaI7GOU'
# artist = sp.artist(artistID)
# artistTopTracks = sp.artist_top_tracks(artistID)
# # pprint.pprint(artist)
# # pprint.pprint(len(artistTopTracks['tracks']))

# tracks = artistTopTracks['tracks']
# trackNames = []
# for x in tracks: #10번 돌겠지?
#     trackNames.append(x['album']['name'])

# print(trackNames)



import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pprint

client_id = '6b25f06078274ba5b42eb8308bf107ce'
client_secret = '10a43a425e5e4a229ce7ba63f60a0374'

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 PANDAS로 데이터프레임으로 만드는 과정입니다.

artist_name =[]
track_name = []
track_popularity =[]
artist_id =[]
track_id =[]
track_images = []

# result = sp.search(q='year:2024', type='track', market='KR', limit=10, offset=i)
# tracks = result['tracks']['items']
# trackNames = []
# for i in tracks:
#     trackNames.append(i['album']['name'])

# print(trackNames)

for i in range(0,100,50):
    track_results = sp.search(q='year:2024', type='track', market='KR', limit=50, offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        track_popularity.append(t['popularity'])
        track_images.append(t['album']['images'][0]['url'])

# for x,y in zip(artist_name, track_name):
#     print(x,' - ',y)
        
track_df = pd.DataFrame({'track_name' : track_name, 'track_id' : track_id, 'track_popularity' : track_popularity, 'artist_name' : artist_name, 'artist_id' : artist_id, 'track_image_link': track_images})