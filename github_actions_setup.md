# GitHub Actions setup for weekly playlist updates

The workflow in `.github/workflows/update-playlist.yml` runs every **Monday at 00:00 UTC** and can also be triggered manually from the Actions tab.

## Required repository secrets

In your GitHub repo go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `SPOTIPY_CLIENT_ID` | Your Spotify app Client ID |
| `SPOTIPY_CLIENT_SECRET` | Your Spotify app Client Secret |
| `SPOTIPY_REDIRECT_URI` | Redirect URI (e.g. `http://localhost:8080`) |
| `SPOTIPY_CACHE` | Cached Spotify token so the job can run without a browser (see below) |

## One-time: create the Spotify auth cache

The script uses Spotify OAuth, which normally opens a browser. In CI there is no browser, so you must create a token once on your machine and store it as the `SPOTIPY_CACHE` secret.

1. **Run the script locally** (with your `.env` set up):
   ```bash
   python weekly_mix_review.py
   ```
   Complete the browser login when prompted.

2. **Find the cache file**  
   Spotipy saves the token to a file named `.cache` (or `.cache-<username>`) in the project directory. If you don’t see it, check that the script ran and that your user has write access to the project folder.

3. **Add the cache as the `SPOTIPY_CACHE` secret**  
   **Option A (recommended):** Base64-encode the file so newlines and special characters are preserved. In the project directory:
   ```bash
   # Linux/macOS
   base64 -w0 .cache
   ```
   Copy the output and paste it as the value of the `SPOTIPY_CACHE` repository secret.  
   **Option B:** Open the `.cache` file, copy its **entire contents** (JSON), and paste that as the value of `SPOTIPY_CACHE`. If the workflow fails with auth errors, use Option A instead.  
   **Windows (PowerShell):** To base64-encode: `[Convert]::ToBase64String([IO.File]::ReadAllBytes(".cache"))`

4. **Optional: use a fixed cache path locally**  
   To force the cache file to be named `.cache` (so you always know which file to copy), you can run with:
   ```bash
   set SPOTIPY_CACHE_PATH=.cache
   python weekly_mix_review.py
   ```
   (On macOS/Linux use `export SPOTIPY_CACHE_PATH=.cache`.)

Tokens expire after a while. If the workflow starts failing with auth errors, run the script locally again, re-copy the new cache contents into the `SPOTIPY_CACHE` secret, and re-run the workflow.

## Manual run

Open your repo on GitHub → **Actions** → **Update weekly playlist** → **Run workflow**.
