from __future__ import annotations

from src.common.config import load_yaml


def load_metric_definitions() -> list[dict]:
    """Load metric definitions."""
    return load_yaml("config/metric_definitions.yaml")["metrics"]
