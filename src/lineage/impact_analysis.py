from __future__ import annotations

from src.semantic.metric_loader import load_metric_definitions


def impacted_consumers(metric_name: str) -> list[str]:
    """Return downstream consumers for a metric."""
    for metric in load_metric_definitions():
        if metric["metric_name"] == metric_name:
            return list(metric["allowed_consumers"])
    return []
