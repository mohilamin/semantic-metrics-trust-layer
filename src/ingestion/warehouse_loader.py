from __future__ import annotations

from src.common.logging import get_logger
from src.ingestion.loaders import load_raw_tables
from src.storage.duckdb_store import write_tables

LOGGER = get_logger(__name__)


def load_warehouse() -> str:
    """Load raw data into the DuckDB warehouse."""
    path = write_tables(load_raw_tables())
    LOGGER.info("warehouse loaded: %s", path)
    return path


if __name__ == "__main__":
    load_warehouse()
