from __future__ import annotations

import pandas as pd

from src.semantic.metric_loader import load_metric_definitions
from src.semantic.model_loader import load_semantic_models


def validate_semantic_layer() -> pd.DataFrame:
    """Validate that metric source tables are represented in semantic models."""
    models = load_semantic_models()["models"]
    available_sources = set(models)
    rows = []
    aliases = {
        "orders": "order",
        "invoices": "invoice",
        "payments": "payment",
        "subscriptions": "subscription",
        "support_tickets": "support",
        "marketing_campaigns": "marketing",
        "sales_opportunities": "sales",
        "web_events": "marketing",
        "customers": "customer",
        "accounts": "account",
        "refunds": "payment",
        "products": "order",
    }
    for metric in load_metric_definitions():
        mapped = {aliases.get(source, source) for source in metric["source_tables"]}
        missing = sorted(mapped - available_sources)
        rows.append(
            {
                "metric_id": metric["metric_id"],
                "metric_name": metric["metric_name"],
                "status": "pass" if not missing else "fail",
                "missing_models": ",".join(missing),
            }
        )
    return pd.DataFrame(rows)
