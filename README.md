# Weekly Radar Mix

[![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Update weekly playlist](https://github.com/vsapiens/weekly-radar-mix/actions/workflows/update-playlist.yml/badge.svg)](https://github.com/vsapiens/weekly-radar-mix/actions/workflows/update-playlist.yml)
[![Changelog](https://img.shields.io/badge/changelog-keep%20a%20changelog-orange)](CHANGELOG.md)

> Automatically build and refresh a Spotify playlist with tracks from any genres you like — every week, hands-free.

Fork this repo, configure two secrets, and your personal radar mix will update itself every Monday (or whenever you trigger it). Customize the genres, schedule, and track count entirely from the command line or environment variables — no code editing required.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage & CLI Flags](#usage--cli-flags)
- [Customization](#customization)
- [GitHub Actions Setup](#github-actions-setup)
- [Maintenance](#maintenance)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## Features

- **Automated weekly refresh** via GitHub Actions (every Monday 00:00 UTC)
- **Manual trigger** from the Actions tab with optional dry-run mode
- **Fully configurable** genres, track limits, and playlist — via CLI flags or env vars
- **Dry-run mode** to preview the track list before committing any changes
- **Verbose output** to see artist + track names during a run
- **Duplicate filtering** across genre queries
- **Randomized order** for variety each week
- **Headless CI/CD auth** via a cached OAuth token — no browser required in automation
- **Zero lock-in** — plain Python, no proprietary frameworks

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                        │
│  Schedule (Monday) ──┐                                  │
│  Manual trigger   ───┼──▶  weekly_mix_review.py         │
│                       │         │                        │
│                       │    1. Authenticate (cached token)│
│                       │    2. Search tracks per genre    │
│                       │    3. Deduplicate + shuffle      │
│                       │    4. Replace playlist           │
└───────────────────────────────────────────────────────-──┘
                                  │
                                  ▼
                         Spotify Playlist ✓
```

The script uses the **Spotify Search API** to fetch up to N tracks for each genre query, deduplicates across queries, shuffles the result, then atomically replaces the target playlist.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/vsapiens/weekly-radar-mix.git
cd weekly-radar-mix

# 2. Install
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your Spotify credentials

# 4. Run (dry-run first to verify)
python weekly_mix_review.py --dry-run
python weekly_mix_review.py
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.9+** | Earlier versions may work but are untested |
| **Spotify account** | Free or Premium |
| **Spotify Developer app** | Free — create at [developer.spotify.com](https://developer.spotify.com/dashboard) |
| **A Spotify playlist** | Create one from the app and copy its ID |

### Create a Spotify Developer App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click **Create app**.
3. Set any name/description; for **Redirect URI** add `http://localhost:8080/callback`.
4. Save. Copy your **Client ID** and **Client Secret**.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/vsapiens/weekly-radar-mix.git
cd weekly-radar-mix

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

**Developers** (linting + formatting tools):

```bash
pip install -r requirements-dev.txt
```

Or use Make:

```bash
make install        # production deps only
make dev-install    # production + dev deps
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `SPOTIPY_CLIENT_ID` | Yes | Your Spotify app's Client ID |
| `SPOTIPY_CLIENT_SECRET` | Yes | Your Spotify app's Client Secret |
| `SPOTIPY_REDIRECT_URI` | Yes | OAuth callback URI — must match your app settings |
| `SPOTIPY_PLAYLIST_ID` | Yes | Spotify playlist ID, URI, or share URL to update |
| `DRY_RUN` | No | Set to `1`, `true`, or `yes` to preview without changes |

**Finding your playlist ID:** Open Spotify → right-click your playlist → Share → Copy link to playlist.
The ID is the string after `/playlist/` and before `?`.

---

## Usage & CLI Flags

```
python weekly_mix_review.py [OPTIONS]
```

| Flag | Short | Default | Description |
|---|---|---|---|
| `--dry-run` | `-n` | `$DRY_RUN` env | Preview track list without updating the playlist |
| `--genres QUERY …` | `-g` | 5 built-in queries | One or more Spotify search queries |
| `--limit N` | `-l` | `15` | Tracks to fetch per query (1–50, Spotify API max) |
| `--playlist ID` | `-p` | `$SPOTIPY_PLAYLIST_ID` env | Playlist ID, URI, or share URL |
| `--verbose` | `-v` | off | Print artist – track name for every result |

### Examples

```bash
# Normal run — update the playlist
python weekly_mix_review.py

# Preview what would be added (no changes)
python weekly_mix_review.py --dry-run

# Custom genres
python weekly_mix_review.py --genres "salsa hits" "bachata romantica" "cumbia moderna"

# 30 tracks per genre with verbose output
python weekly_mix_review.py --limit 30 --verbose

# Target a different playlist
python weekly_mix_review.py --playlist 417YNUWmPJcvGknVUQaW14

# Full custom run — short flags
python weekly_mix_review.py -g "afrobeats 2025" "amapiano" -l 20 -p <PLAYLIST_ID> -nv

# Override genre via environment variable (useful in scripts)
SPOTIPY_PLAYLIST_ID=<ID> DRY_RUN=1 python weekly_mix_review.py
```

---

## Customization

### Change the default genres

Pass `--genres` on the command line or edit `DEFAULT_GENRES` in `weekly_mix_review.py`:

```python
DEFAULT_GENRES = [
    "afrobeats 2025",
    "amapiano hits",
    "drill uk",
    "dancehall new",
    "kuduro angolano",
]
```

### Change the weekly schedule

Edit `.github/workflows/update-playlist.yml`:

```yaml
on:
  schedule:
    - cron: "0 8 * * 5"   # Every Friday at 08:00 UTC
```

Use [crontab.guru](https://crontab.guru) to build your schedule expression.

### Change the number of tracks

```bash
# Fetch 50 tracks per genre (maximum)
python weekly_mix_review.py --limit 50
```

Or set a permanent default by editing the `default=15` value in `weekly_mix_review.py`.

---

## GitHub Actions Setup

The workflow at `.github/workflows/update-playlist.yml` runs automatically.
To set it up for your fork:

### Step 1 — Spotify Developer App redirect URI

In your [Spotify Dashboard](https://developer.spotify.com/dashboard) app settings add:

```
https://example.com/callback
```

### Step 2 — Generate an OAuth token (one time)

Run locally to produce a token JSON for CI:

```bash
python setup_token.py
```

The script opens your browser, you log in, paste back the redirect URL, and it prints a JSON blob.

### Step 3 — Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name | Value |
|---|---|
| `SPOTIPY_CLIENT_ID` | Your app's Client ID |
| `SPOTIPY_CLIENT_SECRET` | Your app's Client Secret |
| `SPOTIPY_REDIRECT_URI` | `https://example.com/callback` |
| `SPOTIPY_PLAYLIST_ID` | Your playlist ID |
| `SPOTIFY_TOKEN_CACHE` | The JSON printed by `setup_token.py` |

### Step 4 — Test the workflow

1. Go to **Actions → Update weekly playlist → Run workflow**.
2. Enable **Dry run** for a safe first test.
3. Confirm the log shows `[DRY RUN] Would update playlist with N tracks`.
4. Run again without **Dry run** to update the playlist live.

---

## Maintenance

### Token refresh

The Spotify OAuth token includes a refresh token. The script and Spotipy library handle token renewal automatically. If the workflow starts failing with authentication errors:

1. Run `python setup_token.py` locally again.
2. Update the `SPOTIFY_TOKEN_CACHE` GitHub Secret with the new JSON.

### Dependency updates

```bash
# Review outdated packages
pip list --outdated

# Update and re-pin
pip install --upgrade spotipy python-dotenv
pip freeze | grep -E "^(spotipy|python-dotenv)" > requirements.txt
```

### Creating a release

Tag a release so your users can pin to a known-good version:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Then create a GitHub Release from that tag with release notes from [CHANGELOG.md](CHANGELOG.md).

---

## Project Structure

```
weekly-radar-mix/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md          # Bug report template
│   │   └── feature_request.md     # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md   # PR checklist
│   └── workflows/
│       └── update-playlist.yml    # Scheduled + manual CI/CD workflow
├── .env.example                   # Environment variable template
├── .gitignore
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # Contribution guide
├── LICENSE                        # MIT license
├── Makefile                       # Developer shortcuts
├── README.md                      # This file
├── SECURITY.md                    # Security policy
├── github_actions_setup.md        # Detailed Actions setup guide
├── requirements.txt               # Production dependencies
├── requirements-dev.txt           # Developer/linting dependencies
├── setup_token.py                 # One-time OAuth token generator
└── weekly_mix_review.py           # Main script
```

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ideas for contributions:**
- Support for Spotify recommendations API (seed-based discovery)
- Reading genre queries from a config file (`genres.txt`)
- Multiple playlist targets in one run
- Statistics output (BPM range, popularity distribution)
- Tests with mocked Spotipy responses

---

## Security

Never commit your `.env` file or `.cache` token file. See [SECURITY.md](SECURITY.md) for the full security policy and how to report vulnerabilities privately.

---

## License

[MIT](LICENSE) © vsapiens
