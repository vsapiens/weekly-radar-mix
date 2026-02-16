# GitHub Actions setup for weekly playlist updates

The workflow runs every **Monday at 00:00 UTC** and can be triggered manually from the Actions tab.

## 1. Spotify Dashboard setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and open your app.
2. In **Redirect URIs**, add exactly: `https://example.com/callback`
3. Save.

## 2. One-time token setup

The script needs a Spotify token to modify your playlist. Run this **once** locally to generate it:

```bash
pip install spotipy python-dotenv
python setup_token.py
```

This will:
- Open your browser to log in to Spotify.
- Redirect to `https://example.com/callback?code=...` (the page won't load — that's expected).
- Copy the **full URL** from the browser address bar and paste it into the terminal.
- Print a JSON token to use as a GitHub Secret.

## 3. Add GitHub Secrets

In your repo go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `SPOTIPY_CLIENT_ID` | Your Spotify app Client ID |
| `SPOTIPY_CLIENT_SECRET` | Your Spotify app Client Secret |
| `SPOTIPY_REDIRECT_URI` | `https://example.com/callback` |
| `SPOTIPY_PLAYLIST_ID` | Playlist ID (e.g. `417YNUWmPJcvGknVUQaW14`) |
| `SPOTIFY_TOKEN_CACHE` | The JSON output from `setup_token.py` |

## 4. Test on GitHub

1. Go to **Actions** → **Update weekly playlist** → **Run workflow**.
2. Check **Dry run** to test without changing the playlist.
3. Confirm the log shows `[DRY RUN] Would update playlist with N tracks`.
4. Run again without **Dry run** to update the playlist for real.

## Refreshing the token

The token includes a refresh token that Spotify uses to get new access tokens automatically. If the workflow starts failing with auth errors, run `python setup_token.py` again locally and update the `SPOTIFY_TOKEN_CACHE` secret.
