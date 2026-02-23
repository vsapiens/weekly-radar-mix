"""
weekly_mix_review.py — Weekly Radar Mix updater for Spotify.

Searches Spotify for tracks matching one or more genre queries, deduplicates
and shuffles the results, then replaces a target playlist with the new mix.

See README.md for full documentation and customisation options.
"""

import os
import random
import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCOPE = "playlist-modify-private playlist-modify-public"
CACHE_PATH = ".cache"

DEFAULT_GENRES = [
    "reggaeton new",
    "latin trap",
    "reggaeton hit",
    "perreo",
    "latin urban",
]


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def track_limit(value: str) -> int:
    """Validate that the --limit value is between 1 and 50 (Spotify API cap)."""
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"limit must be an integer, got {value!r}")
    if not 1 <= n <= 50:
        raise argparse.ArgumentTypeError(
            f"limit must be between 1 and 50 (Spotify API maximum), got {n}"
        )
    return n


parser = argparse.ArgumentParser(
    prog="weekly_mix_review",
    description="Update a Spotify playlist with a curated weekly radar mix.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
examples:
  # Normal run — update the playlist
  python weekly_mix_review.py

  # Dry run — preview without making any changes
  python weekly_mix_review.py --dry-run

  # Custom genres (overrides defaults)
  python weekly_mix_review.py --genres "salsa hits" "bachata romantica"

  # More tracks per query, verbose output
  python weekly_mix_review.py --limit 30 --verbose

  # Target a different playlist
  python weekly_mix_review.py --playlist 417YNUWmPJcvGknVUQaW14

  # Full custom run
  python weekly_mix_review.py -g "afrobeats 2025" "amapiano" -l 20 -p <ID> -nv
""",
)

parser.add_argument(
    "--dry-run", "-n",
    action="store_true",
    default=os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes"),
    help=(
        "preview changes without modifying the playlist "
        "(also controlled by the DRY_RUN environment variable)"
    ),
)

parser.add_argument(
    "--genres", "-g",
    nargs="+",
    metavar="QUERY",
    default=DEFAULT_GENRES,
    help=(
        "one or more Spotify search queries used to discover tracks "
        "(default: %(default)s)"
    ),
)

parser.add_argument(
    "--limit", "-l",
    type=track_limit,
    default=15,
    metavar="N",
    help="tracks to fetch per genre query, 1-50 (default: 15)",
)

parser.add_argument(
    "--playlist", "-p",
    metavar="ID_OR_URI",
    default=None,
    help=(
        "Spotify playlist ID, URI (spotify:playlist:…), or share URL "
        "(overrides the SPOTIPY_PLAYLIST_ID environment variable)"
    ),
)

parser.add_argument(
    "--verbose", "-v",
    action="store_true",
    help="print track names and artists in addition to track IDs",
)

args = parser.parse_args()


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

if os.path.exists(CACHE_PATH):
    # A cached token exists (e.g. restored from a GitHub Secret in CI).
    # Use it so the script can refresh tokens without opening a browser.
    cache_handler = CacheFileHandler(cache_path=CACHE_PATH)
    auth_manager = SpotifyOAuth(scope=SCOPE, cache_handler=cache_handler)
else:
    auth_manager = SpotifyOAuth(scope=SCOPE)

sp = spotipy.Spotify(auth_manager=auth_manager)


# ---------------------------------------------------------------------------
# Resolve playlist ID
# ---------------------------------------------------------------------------

_raw = (args.playlist or os.environ.get("SPOTIPY_PLAYLIST_ID", "")).strip()
if not _raw:
    parser.error(
        "No playlist specified. Use --playlist <ID_OR_URI> or set "
        "the SPOTIPY_PLAYLIST_ID environment variable."
    )

if "open.spotify.com/playlist/" in _raw:
    playlist_id = _raw.split("playlist/")[-1].split("?")[0]
elif _raw.startswith("spotify:playlist:"):
    playlist_id = _raw.split(":")[-1]
else:
    playlist_id = _raw


# ---------------------------------------------------------------------------
# Track discovery
# ---------------------------------------------------------------------------

print(f"Playlist : {playlist_id}")
print(f"Queries  : {args.genres}")
print(f"Limit    : {args.limit} track(s)/query")
print(f"Dry run  : {args.dry_run}")
print()

track_entries: list[tuple[str, str, str]] = []  # (id, name, artist)

for query in args.genres:
    results = sp.search(q=query, type="track", limit=args.limit)
    items = results["tracks"]["items"]
    new_entries = [
        (t["id"], t["name"], t["artists"][0]["name"]) for t in items
    ]
    track_entries.extend(new_entries)
    print(f"  {len(new_entries):>3} tracks found for: {query!r}")


# ---------------------------------------------------------------------------
# Deduplicate (preserve first occurrence) and shuffle
# ---------------------------------------------------------------------------

seen: set[str] = set()
unique_entries: list[tuple[str, str, str]] = []
for entry in track_entries:
    if entry[0] not in seen:
        seen.add(entry[0])
        unique_entries.append(entry)

random.shuffle(unique_entries)

track_ids = [e[0] for e in unique_entries]

print(f"\nTotal unique tracks: {len(track_ids)}")

if args.verbose and unique_entries:
    print("\nTrack list:")
    for i, (_, name, artist) in enumerate(unique_entries, 1):
        print(f"  {i:>3}. {artist} – {name}")


# ---------------------------------------------------------------------------
# Apply changes (or skip in dry-run mode)
# ---------------------------------------------------------------------------

if args.dry_run:
    print(
        f"\n[DRY RUN] Would update playlist {playlist_id} "
        f"with {len(track_ids)} tracks (no changes made)."
    )
elif not track_ids:
    print("\nNo tracks found. Playlist was not changed.")
else:
    sp.playlist_replace_items(playlist_id, [])
    sp.playlist_add_items(playlist_id, track_ids)
    print(f"\nUpdated playlist {playlist_id} with {len(track_ids)} tracks.")
