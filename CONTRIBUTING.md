# Contributing to Weekly Radar Mix

Thank you for your interest in improving this project. Contributions of all kinds are welcome — bug reports, feature ideas, documentation improvements, and code changes.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Running Locally](#running-locally)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Ideas for Contribution](#ideas-for-contribution)

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:

   ```bash
   git clone https://github.com/<your-username>/weekly-radar-mix.git
   cd weekly-radar-mix
   ```

3. **Add the upstream remote** so you can keep in sync:

   ```bash
   git remote add upstream https://github.com/vsapiens/weekly-radar-mix.git
   ```

4. **Create a branch** for your change:

   ```bash
   git checkout -b feat/my-improvement
   ```

---

## Development Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate       # Windows

# Install all dependencies (production + dev tools)
make dev-install
# or: pip install -r requirements.txt -r requirements-dev.txt

# Copy environment template
cp .env.example .env
# Edit .env with your Spotify credentials
```

---

## Running Locally

```bash
# Dry run — preview without changing the playlist
make dry-run
# or: python weekly_mix_review.py --dry-run

# Normal run
make run
# or: python weekly_mix_review.py

# Custom genres test
python weekly_mix_review.py --genres "jazz fusion" "neo soul" --limit 10 --dry-run --verbose
```

---

## Code Style

This project uses:

- **[Black](https://black.readthedocs.io/)** for formatting (line length 88)
- **[Flake8](https://flake8.pycqa.org/)** for linting

```bash
make format   # auto-format with Black
make lint     # check with Flake8
```

Please run both before opening a pull request. CI will check formatting and linting automatically.

---

## Submitting Changes

1. Ensure your branch is up to date with upstream `main`:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Run a dry-run to confirm your changes work:

   ```bash
   python weekly_mix_review.py --dry-run --verbose
   ```

3. Commit with a descriptive message:

   ```bash
   git commit -m "feat: support reading genres from genres.txt config file"
   ```

4. Push and open a Pull Request against `main`.

5. Fill in the PR template — describe what changed and why, and check all items in the checklist.

### Commit message conventions

Use the format `type: short description`:

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure, no behavior change |
| `chore` | Dependency updates, CI changes |

---

## Ideas for Contribution

Looking for something to work on? Here are open directions:

- **Recommendations API** — use `sp.recommendations()` with seed tracks/genres instead of keyword search for better music discovery
- **Genre config file** — read search queries from a `genres.txt` (one per line) so users never need to touch Python
- **Multiple playlists** — support a list of `PLAYLIST_ID` values and update them all in one run
- **Statistics output** — show popularity range, BPM stats, or top artists discovered
- **Tests** — add `pytest` tests with a mocked Spotipy client so the core logic can be tested offline
- **Windows `make` support** — provide a `Makefile.ps1` or `tasks.json` for VS Code users on Windows
- **Token auto-refresh detection** — warn in the workflow log when the cached token is close to expiry
