# Weekly Radar Mix — developer shortcuts
# Run `make` or `make help` to see available targets.

.PHONY: help install dev-install run dry-run setup-token lint format clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev-install: ## Install production + developer dependencies
	pip install -r requirements.txt -r requirements-dev.txt

run: ## Update the Spotify playlist (reads credentials from .env)
	python weekly_mix_review.py

dry-run: ## Preview tracks without updating the playlist
	python weekly_mix_review.py --dry-run

verbose: ## Preview tracks with full artist/title output
	python weekly_mix_review.py --dry-run --verbose

setup-token: ## Generate an OAuth token for GitHub Actions CI/CD (run once)
	python setup_token.py

lint: ## Check code style with Flake8
	flake8 weekly_mix_review.py setup_token.py

format: ## Auto-format code with Black
	black weekly_mix_review.py setup_token.py

clean: ## Remove cache files and compiled Python bytecode
	rm -f .cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

.DEFAULT_GOAL := help
