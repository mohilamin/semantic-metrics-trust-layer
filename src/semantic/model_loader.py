from __future__ import annotations

from src.common.config import load_yaml


def load_semantic_models() -> dict:
    """Load semantic models."""
    return load_yaml("config/semantic_models.yaml")
