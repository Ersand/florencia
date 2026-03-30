.PHONY: help install lint fix check test clean run api cli pre-commit-hooks format setup

help:
	@echo "Available targets:"
	@echo "  install           - Install project with uv"
	@echo "  setup             - Full setup (install + pre-commit)"
	@echo "  lint              - Run ruff linter"
	@echo "  fix               - Fix linting issues with ruff"
	@echo "  format            - Format code with ruff"
	@echo "  check             - Run ruff, mypy, and pydantic checks"
	@echo "  test              - Run pytest with coverage"
	@echo "  clean             - Remove build artifacts and cache"
	@echo "  run               - Run CLI (scraper)"
	@echo "  api               - Run FastAPI server"
	@echo "  pre-commit-hooks  - Run pre-commit hooks manually"

install:
	uv sync --all-extras

setup: install
	uv run pre-commit install
	@echo "Setup complete!"

lint:
	ruff check .

fix:
	ruff check --fix .

format:
	ruff format .

mypy:
	uv run mypy florencia/

check: lint mypy

test:
	uv run pytest

clean:
	rm -rf build/ dist/ *.egg-info .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run:
	uv run florencia scrape

api:
	uv run uvicorn florencia.main:app --reload --host 0.0.0.0 --port 8080

pre-commit-hooks:
	uv run pre-commit run --all-files

bump-version:
	@echo "Usage: uv bump"
