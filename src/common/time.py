from __future__ import annotations

from datetime import UTC, datetime


def utc_now_iso() -> str:
    """Return current UTC timestamp."""
    return datetime.now(UTC).isoformat()
