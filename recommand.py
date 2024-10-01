import spotipy
import pandas as pd
import seaborn as sn
import pprint
import plotly.graph_objects as go
import plotly.offline as pyo
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn import preprocessing

client_id = '6b25f06078274ba5b42eb8308bf107ce'
client_secret = '10a43a425e5e4a229ce7ba63f60a0374'
client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

print(sp.artist('3PhoLpVuITZKcymswpck5b')['name'], ' - ',sp.tracks('1r9xUipOqoNwggBpENDsvJ'))

rec = sp.recommendations(seed_artists=["3PhoLpVuITZKcymswpck5b"], seed_genres=["pop"], seed_tracks=["1r9xUipOqoNwggBpENDsvJ"], limit=10)

for track in rec['tracks']:
    print(track['artists'][0]['name'], track['name'])
