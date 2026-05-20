from __future__ import annotations

from src.lineage.lineage_builder import build_lineage


def export_graph() -> dict[str, object]:
    """Export lineage graph JSON."""
    _, _, graph = build_lineage()
    return graph
