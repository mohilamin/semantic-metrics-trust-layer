from __future__ import annotations

import duckdb
import pandas as pd

from src.common.paths import ensure_dir, project_path


def warehouse_path() -> str:
    """Return the local DuckDB path."""
    ensure_dir(project_path("data/warehouse"))
    return str(project_path("data/warehouse/semantic_metrics.duckdb"))


def write_tables(frames: dict[str, pd.DataFrame]) -> str:
    """Write pandas dataframes to DuckDB tables."""
    path = warehouse_path()
    with duckdb.connect(path) as con:
        for name, frame in frames.items():
            con.register("_frame", frame)
            con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM _frame")
            con.unregister("_frame")
    return path


def query(sql: str) -> pd.DataFrame:
    """Run a query against the local warehouse."""
    with duckdb.connect(warehouse_path()) as con:
        return con.execute(sql).df()
