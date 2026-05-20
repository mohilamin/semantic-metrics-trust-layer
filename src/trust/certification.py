from __future__ import annotations

from src.semantic.metric_loader import load_metric_definitions


def certified_metric_names() -> list[str]:
    """Return certified metric names."""
    return [metric["metric_name"] for metric in load_metric_definitions() if metric["certification_status"] == "certified"]
