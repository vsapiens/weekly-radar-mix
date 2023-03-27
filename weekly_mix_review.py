import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

os.environ["SPOTIPY_CLIENT_ID"] = os.environ.get("SPOTIPY_CLIENT_ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = os.environ.get("SPOTIPY_CLIENT_SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = os.environ.get("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))

user_id = sp.me()["id"]

playlist_id = "417YNUWmPJcvGknVUQaW14"
genres = ["latin urban", "urban", "trap", "reggaeton"]

track_ids = []

# Search for tracks with the desired genres
for genre in genres:
    search_results = sp.search(q=f'genre:"{genre}"', type="track", limit=10)
    genre_track_ids = [track["id"] for track in search_results["tracks"]["items"]]
    track_ids.extend(genre_track_ids)

# Shuffle the tracks to create a more diverse playlist
random.shuffle(track_ids)

# Clear the existing playlist
sp.playlist_replace_items(playlist_id, [])

# Add tracks to the existing playlist
sp.playlist_add_items(playlist_id, track_ids)

print(f"Updated the playlist with {len(track_ids)} tracks.")
