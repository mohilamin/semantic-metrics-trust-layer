from __future__ import annotations

import pandas as pd


def detect_metric_anomalies(metrics: pd.DataFrame) -> pd.DataFrame:
    """Flag simple metric anomalies."""
    output = metrics.copy()
    output["anomaly_flag"] = output["metric_value"].abs() > output["metric_value"].abs().quantile(0.99)
    return output
