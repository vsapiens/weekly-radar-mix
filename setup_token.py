"""
One-time setup: generates a Spotify OAuth token for GitHub Actions.

Run this locally once. It will:
1. Open a browser to log in to Spotify.
2. Redirect to https://example.com/callback?code=...
3. You paste that full URL here.
4. It prints the token JSON to add as the SPOTIFY_TOKEN_CACHE secret.

Usage:
    python setup_token.py
"""

import os
import json
import webbrowser
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = "playlist-modify-private playlist-modify-public"

auth_manager = SpotifyOAuth(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
    scope=SCOPE,
    open_browser=False,
)

auth_url = auth_manager.get_authorize_url()

print()
print("=" * 60)
print("Open this URL in your browser to log in to Spotify:")
print()
print(f"  {auth_url}")
print()
print("After approving, the browser will redirect to a URL like:")
print("  https://example.com/callback?code=AQD...")
print("(The page won't load — that's expected.)")
print("=" * 60)
print()

webbrowser.open(auth_url)

redirect_url = input("Paste the full redirect URL here: ").strip()

code = auth_manager.parse_response_code(redirect_url)
token_info = auth_manager.get_access_token(code, as_dict=True)

cache_json = json.dumps(token_info)

print()
print("=" * 60)
print("SUCCESS! Copy the JSON below and add it as a GitHub Secret")
print("named SPOTIFY_TOKEN_CACHE:")
print("=" * 60)
print()
print(cache_json)
print()
print("Go to: https://github.com/<your-repo>/settings/secrets/actions")
print("Click 'New repository secret', name it SPOTIFY_TOKEN_CACHE,")
print("and paste the JSON above as the value.")
