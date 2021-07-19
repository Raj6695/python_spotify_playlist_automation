from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import spotipy

SPOTIPY_CLIENT_ID = "ID"
SPOTIPY_CLIENT_SECRET = "SECRET"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]
print(song_names)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"


    )
)
songs = []
user_id = sp.current_user()["id"]
year = date.split("-")[0]
print(user_id)
play = sp.user_playlist_create(user=user_id, name=f"{date} POPULAR-songs", public=False)
print(play["id"])
for items in song_names:
    get_song = sp.search(q=f"track:{items} year:{year}", type="track")

    uri = (get_song["tracks"]["items"][0]["uri"])
    songs.append(uri)

playlist_synthesis = sp.playlist_add_items(playlist_id=play["id"], items=songs)

popular = sp.artist_top_tracks(artist_id="7dGJo4pcD2V6oG8kP0tJRR", country="US")

for num in range(len(popular["tracks"])):
    songs.append(popular["tracks"][num]["uri"])
plays = sp.playlist_add_items(playlist_id=play["id"], items=songs)
print(plays)
