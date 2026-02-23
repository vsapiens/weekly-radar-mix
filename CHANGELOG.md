# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] - 2026-02-23

### Added
- **CLI flags** — `--dry-run` (`-n`), `--genres` (`-g`), `--limit` (`-l`),
  `--playlist` (`-p`), `--verbose` (`-v`) via `argparse`
- `--limit` validates 1–50 range (Spotify API maximum)
- `--playlist` accepts playlist ID, `spotify:playlist:…` URI, or share URL
- `--verbose` prints artist – track name for every discovered track
- `--genres` overrides default search queries at runtime without editing code
- `DEFAULT_GENRES` constant for easy script-level customization
- `Makefile` with `help`, `install`, `dev-install`, `run`, `dry-run`,
  `setup-token`, `lint`, `format`, `clean` targets
- `CONTRIBUTING.md` — contribution guide and development workflow
- `SECURITY.md` — security policy and credential hygiene guidelines
- `CHANGELOG.md` — this file
- `LICENSE` — MIT license (was referenced in README but missing)
- `requirements-dev.txt` — `flake8` and `black` for code quality
- `.github/ISSUE_TEMPLATE/bug_report.md` — structured bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` — feature request template
- `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist
- pip dependency caching in GitHub Actions workflow (faster CI runs)
- Comprehensive README rewrite: badges, table of contents, architecture
  diagram, full CLI reference, customization guide, maintenance section

### Changed
- `weekly_mix_review.py` restructured with clear sections (constants, auth,
  CLI parsing, track discovery, deduplication, apply)
- Playlist ID resolution now also handles `spotify:playlist:…` URIs
- Verbose track listing uses index numbers for readability
- GitHub Actions workflow step names clarified; pip cache added

### Fixed
- Script now exits with a clear error message when no playlist is specified
  (instead of silently using a hardcoded fallback ID)

---

## [0.1.0] - 2026-02-16

### Added
- Initial automated Spotify playlist updater using the Search API
- Weekly schedule via GitHub Actions (every Monday 00:00 UTC)
- Manual `workflow_dispatch` trigger with `dry_run` boolean input
- OAuth 2.0 Spotify authentication with file-based token caching
- Headless CI/CD support: token cache restored from `SPOTIFY_TOKEN_CACHE`
  GitHub Secret using `printf` to handle JSON safely
- Track discovery across 5 default genre queries (15 tracks each)
- Duplicate filtering across genre searches
- Random shuffle for weekly variety
- `setup_token.py` — one-time local OAuth token generator for CI setup
- `github_actions_setup.md` — step-by-step Actions setup guide
- `.env.example` with all required variables documented

---

[Unreleased]: https://github.com/vsapiens/weekly-radar-mix/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vsapiens/weekly-radar-mix/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/vsapiens/weekly-radar-mix/releases/tag/v0.1.0
