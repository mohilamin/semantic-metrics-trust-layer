from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from src.common.paths import project_path


@lru_cache(maxsize=32)
def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file from the project."""
    full_path = Path(path)
    if not full_path.is_absolute():
        full_path = project_path(str(path))
    return yaml.safe_load(full_path.read_text(encoding="utf-8")) or {}


def settings() -> dict[str, Any]:
    """Load project settings."""
    return load_yaml("config/settings.yaml")
