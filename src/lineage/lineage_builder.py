from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.semantic.metric_loader import load_metric_definitions


def build_lineage() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    """Build metric lineage nodes and edges."""
    nodes: list[dict[str, object]] = []
    edges: list[dict[str, object]] = []
    graph: dict[str, object] = {"metrics": []}
    for metric in load_metric_definitions():
        nodes.append({"node_id": metric["metric_name"], "node_type": "metric", "owner": metric["owner"], "impact_level": "high"})
        lineage = {
            "metric_id": metric["metric_id"],
            "metric_name": metric["metric_name"],
            "source_tables": metric["source_tables"],
            "source_columns": ["synthetic business columns"],
            "transformations": [metric["formula"]],
            "downstream_consumers": metric["allowed_consumers"],
            "dashboards": [consumer for consumer in metric["allowed_consumers"] if "dashboard" in consumer],
            "ai_agents": ["enterprise_metric_agent"] if metric["ai_agent_allowed_flag"] else [],
            "owner": metric["owner"],
            "impact_level": "high" if metric["domain"] in ["finance", "operations"] else "medium",
        }
        graph["metrics"].append(lineage)
        for table in metric["source_tables"]:
            nodes.append({"node_id": table, "node_type": "source_table", "owner": metric["owner"], "impact_level": "source"})
            edges.append({"source": table, "target": metric["metric_name"], "relationship": "feeds_metric"})
        for consumer in metric["allowed_consumers"]:
            nodes.append({"node_id": consumer, "node_type": "consumer", "owner": metric["owner"], "impact_level": "consumer"})
            edges.append({"source": metric["metric_name"], "target": consumer, "relationship": "consumed_by"})
    out = ensure_dir(project_path("data/lineage"))
    nodes_df = pd.DataFrame(nodes).drop_duplicates("node_id")
    edges_df = pd.DataFrame(edges)
    nodes_df.to_csv(out / "metric_lineage_nodes.csv", index=False)
    edges_df.to_csv(out / "metric_lineage_edges.csv", index=False)
    (out / "metric_lineage.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    return nodes_df, edges_df, graph
