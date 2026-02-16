# GitHub Actions setup for weekly playlist updates

The workflow in `.github/workflows/update-playlist.yml` runs every **Monday at 00:00 UTC** and can also be triggered manually from the Actions tab.

## Testing on GitHub

Before relying on the scheduled run, test the workflow manually:

1. **Add all required secrets** (see below).
2. Go to **Actions** → **Update weekly playlist** → **Run workflow**.
3. Turn **Dry run** on (checkbox) so the job only logs what it would do and does not change the playlist.
4. Click **Run workflow** and confirm the run succeeds and the log shows e.g. `[DRY RUN] Would update playlist with N tracks`.
5. Run again with **Dry run** off to update the playlist for real (or leave it to the Monday schedule).

**Note:** The script uses Spotify OAuth, which requires a browser to log in. GitHub Actions has no browser, so the workflow will not be able to complete authentication when run in CI. Use the workflow for local/manual runs only, or add a token-based auth strategy if you need unattended runs.

## Required repository secrets

In your GitHub repo go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `SPOTIPY_CLIENT_ID` | Your Spotify app Client ID |
| `SPOTIPY_CLIENT_SECRET` | Your Spotify app Client Secret |
| `SPOTIPY_REDIRECT_URI` | Redirect URI (e.g. `http://localhost:8080`) |
| `SPOTIPY_PLAYLIST_ID` | Optional. Playlist ID or full Spotify playlist URI to update. If unset, script uses default. |

## Manual run

Open your repo on GitHub → **Actions** → **Update weekly playlist** → **Run workflow**. Choose **Dry run** to test without changing the playlist; scheduled runs (Mondays) always update the playlist.
