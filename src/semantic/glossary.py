from __future__ import annotations

from src.semantic.metric_loader import load_metric_definitions


def build_glossary() -> list[dict[str, str]]:
    """Build a simple metric glossary from definitions."""
    return [
        {
            "metric_name": metric["metric_name"],
            "business_definition": metric["business_definition"],
            "owner": metric["owner"],
            "domain": metric["domain"],
        }
        for metric in load_metric_definitions()
    ]
