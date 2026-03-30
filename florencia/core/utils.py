"""Utility functions for the application."""

from pathlib import Path


def ensure_dir(path: Path | str) -> Path:
    """Ensure directory exists, create if not."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get data directory."""
    return get_project_root() / "data"
