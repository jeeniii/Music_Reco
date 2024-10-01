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

# 트랙 가져오기
artist_name =[]
track_name = []
track_popularity =[]
artist_id =[]
track_id =[]

for i in range(0,1000,50):
    track_results = sp.search(q='year:2024', type='track', market='KR', limit=50, offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        artist_id.append(t['artists'][0]['id'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        track_popularity.append(t['popularity'])

# 데이터프레임으로 변환
track_df = pd.DataFrame({'track_name' : track_name, 'track_id' : track_id, 'track_popularity' : track_popularity, 'artist_name' : artist_name, 'artist_id' : artist_id})
print(track_df.shape)
track_df.head()

# 아티스트 데이터 추출
artist_popularity = []
artist_genres = []
artist_followers =[]

for a_id in track_df.artist_id:
    artist = sp.artist(a_id)
    artist_popularity.append(artist['popularity'])
    artist_genres.append(artist['genres'])
    artist_followers.append(artist['followers']['total'])

track_df = track_df.assign(artist_popularity = artist_popularity, artist_genres = artist_genres, artist_followers = artist_followers)
track_df.head()

# 오디오 데이터 추출
track_features = []

for t_id in track_df['track_id']:
    af = sp.audio_features(t_id)
    track_features.append(af)

tf_df = pd.DataFrame(columns = ['acousticness', 'analysis_url', 'danceability', 'duration_ms', 'energy', 'id', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'track_href', 'type', 'uri', 'valence'])

for item in track_features:
    for feat in item:
        feat_df = pd.DataFrame([feat])
        tf_df = pd.concat([tf_df,feat_df], ignore_index=True)

tf_df.head()

cols_to_drop2 = ['key','mode','type', 'uri','track_href','analysis_url']
tf_df = tf_df.drop(columns=cols_to_drop2)

track_df['track_name'] = track_df['track_name'].astype('string')
track_df['artist_name'] = track_df['artist_name'].astype('string')
track_df['track_id'] = track_df['track_id'].astype('string')
track_df['artist_id'] = track_df['artist_id'].astype('string')
tf_df['duration_ms'] = pd.to_numeric(tf_df['duration_ms'])
tf_df['instrumentalness'] = pd.to_numeric(tf_df['instrumentalness'])
tf_df['time_signature'] = tf_df['time_signature'].astype('category')

track_df.sort_values(by=['track_popularity'], ascending=False)[['track_name', 'artist_name']].drop_duplicates().head(10)

by_art_fol = pd.DataFrame(track_df.sort_values(by=['artist_followers'], ascending = False)[['artist_followers','artist_popularity', 'artist_name','artist_genres']])
by_art_fol.astype(str).drop_duplicates().head(10)

def to_1D(series):
    return pd.Series([x for _list in series for x in _list])
to_1D(track_df['artist_genres']).value_counts().head(20)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize = (15,5))
ax.bar(to_1D(track_df['artist_genres']).value_counts().index[:10],to_1D(track_df['artist_genres']).value_counts().values[:10])
ax.set_ylabel('Frequency', size = 10)
ax.set_title('Genres Gantt', size = 15)

top_10_genres = list(to_1D(track_df['artist_genres']).value_counts().index[:10])
top_artist_by_genre = []
for genre in top_10_genres:
    for index, row in by_art_fol.iterrows():
        if genre in row['artist_genres']:
            top_artist_by_genre.append({'artist_name':row['artist_name'], 'artist_genre':genre})
            break
pd.json_normalize(top_artist_by_genre)

# # 예제 DataFrame 생성
# df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# # iterrows를 사용하여 행 반복
# for index, row in df.iterrows():
#     print(index, row['A'], row['B'])

by_track_pop = pd.DataFrame(track_df.sort_values(by=['track_popularity'],ascending=False)[['track_popularity','track_name', 'artist_name','artist_genres', 'track_id']])
by_track_pop.astype(str).drop_duplicates().head(10)
# print(by_track_pop)

top_songs_by_genre = []
for genre in top_10_genres:
    for index, row in by_track_pop.iterrows():
        if genre in row['artist_genres']:
            top_songs_by_genre.append({'track_name':row['track_name'], 'track_popularity':row['track_popularity'],'artist_name':row['artist_name'], 'artist_genre':genre})

pd.json_normalize(top_songs_by_genre).drop_duplicates().head(10)

import seaborn as sn
import matplotlib.pyplot as plt

# 숫자형 열만 선택
numeric_df = tf_df.select_dtypes(include=['float64', 'int64'])

# 히트맵 그리기
sn.set_theme(rc={'figure.figsize': (12, 10)})
sn.heatmap(numeric_df.corr(), annot=True)
plt.show()

sn.set_theme(rc={'figure.figsize':(20,20)})
sn.jointplot(data=tf_df, x='loudness', y='energy', kind='kde')

feat_cols = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
top_100_feat = pd.DataFrame(columns=feat_cols)
for i, track in by_track_pop[:100].iterrows():
    features = tf_df[tf_df['id'] == track['track_id']]
    top_100_feat = pd.concat([top_100_feat, features],ignore_index=True)
top_100_feat = top_100_feat[feat_cols]

mean_vals = pd.DataFrame(columns=feat_cols)
mean_vals = pd.concat([mean_vals, pd.DataFrame([top_100_feat.mean()])], ignore_index=True)
mean_vals = pd.concat([mean_vals, pd.DataFrame([tf_df[feat_cols].mean()])], ignore_index=True)
mean_vals.astype(str).drop_duplicates().head()

fig = go.Figure(
    data=[
        go.Scatterpolar(r=mean_vals.iloc[0], theta=feat_cols, fill='toself', name='Top 100'),
        go.Scatterpolar(r=mean_vals.iloc[1], theta=feat_cols, fill='toself', name='All')
    ],
    layout=go.Layout(
        title = go.layout.Title(text='Feature comparison'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)

fig.show()

rec = sp.recommendations(seed_artists=["3PhoLpVuITZKcymswpck5b"], seed_genres=["pop"], seed_tracks=["1r9xUipOqoNwggBpENDsvJ"], limit=10)
for track in rec['tracks']:
    print(track['artists'][0]['name'], track['name'])