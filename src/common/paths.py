from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def project_path(*parts: str) -> Path:
    """Return a path rooted at the project directory."""
    return PROJECT_ROOT.joinpath(*parts)


def ensure_dir(path: Path) -> Path:
    """Create and return a directory."""
    path.mkdir(parents=True, exist_ok=True)
    return path
