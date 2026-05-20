from __future__ import annotations

import pandas as pd

from src.common.paths import project_path

TABLES = [
    "customers",
    "accounts",
    "orders",
    "invoices",
    "payments",
    "refunds",
    "products",
    "subscriptions",
    "support_tickets",
    "marketing_campaigns",
    "web_events",
    "sales_opportunities",
]


def load_raw_tables() -> dict[str, pd.DataFrame]:
    """Load all raw CSV tables."""
    raw = project_path("data/raw")
    frames: dict[str, pd.DataFrame] = {}
    for table in TABLES:
        path = raw / f"{table}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing raw table: {path}")
        frames[table] = pd.read_csv(path)
    return frames
