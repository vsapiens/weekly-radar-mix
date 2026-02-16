import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from dotenv import load_dotenv

load_dotenv()

os.environ["SPOTIPY_CLIENT_ID"] = os.environ.get("SPOTIPY_CLIENT_ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = os.environ.get("SPOTIPY_CLIENT_SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = os.environ.get("SPOTIPY_REDIRECT_URI")

cache_path = os.environ.get("SPOTIPY_CACHE_PATH")
if cache_path:
    auth_manager = SpotifyOAuth(
        scope="playlist-modify-private",
        cache_handler=CacheFileHandler(cache_path=cache_path),
    )
else:
    auth_manager = SpotifyOAuth(scope="playlist-modify-private")

sp = spotipy.Spotify(auth_manager=auth_manager)

user_id = sp.me()["id"]
#https://open.spotify.com/playlist/417YNUWmPJcvGknVUQaW14?si=decc3064b6df4bab
playlist_id = "417YNUWmPJcvGknVUQaW14"
genres = ["latin urban", "urban", "trap", "reggaeton"]

track_ids = []

# Search for tracks with the desired genres
for genre in genres:
    search_results = sp.search(q=f'genre:"{genre}"', type="track", limit=10)
    genre_track_ids = [track["id"] for track in search_results["tracks"]["items"]]
    track_ids.extend(genre_track_ids)

# Remove duplicates (same track can match multiple genres)
track_ids = list(dict.fromkeys(track_ids))

# Shuffle the tracks to create a more diverse playlist
random.shuffle(track_ids)

dry_run = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
if dry_run:
    print(f"[DRY RUN] Would update playlist with {len(track_ids)} tracks (no changes made).")
else:
    # Clear the existing playlist
    sp.playlist_replace_items(playlist_id, [])
    # Add tracks to the existing playlist
    sp.playlist_add_items(playlist_id, track_ids)
    print(f"Updated the playlist with {len(track_ids)} tracks.")
#