import os
import json
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from dotenv import load_dotenv

load_dotenv()

SCOPE = "playlist-modify-private playlist-modify-public"
CACHE_PATH = ".cache"

# If a .cache file exists (e.g. restored from a secret in CI), use it
# so the script can refresh the token without a browser.
if os.path.exists(CACHE_PATH):
    cache_handler = CacheFileHandler(cache_path=CACHE_PATH)
    auth_manager = SpotifyOAuth(scope=SCOPE, cache_handler=cache_handler)
else:
    auth_manager = SpotifyOAuth(scope=SCOPE)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Playlist ID or full URI from environment
_raw = os.environ.get("SPOTIPY_PLAYLIST_ID", "").strip() or "417YNUWmPJcvGknVUQaW14"
if "open.spotify.com/playlist/" in _raw:
    playlist_id = _raw.split("playlist/")[-1].split("?")[0]
else:
    playlist_id = _raw

# Search terms to discover tracks
search_queries = [
    "reggaeton new",
    "latin trap",
    "reggaeton hit",
    "perreo",
    "latin urban",
]

track_ids = []

# Use the Search API to find tracks by keyword
for query in search_queries:
    results = sp.search(q=query, type="track", limit=15)
    found = [track["id"] for track in results["tracks"]["items"]]
    track_ids.extend(found)
    print(f"  Found {len(found)} tracks for: {query}")

# Remove duplicates (same track can match multiple genres)
track_ids = list(dict.fromkeys(track_ids))

# Shuffle for a more diverse playlist
random.shuffle(track_ids)

print(f"Total unique tracks: {len(track_ids)}")

dry_run = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")
if dry_run:
    print(f"[DRY RUN] Would update playlist with {len(track_ids)} tracks (no changes made).")
elif not track_ids:
    print("No tracks found. Playlist was not changed.")
else:
    sp.playlist_replace_items(playlist_id, [])
    sp.playlist_add_items(playlist_id, track_ids)
    print(f"Updated the playlist with {len(track_ids)} tracks.")