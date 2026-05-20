from __future__ import annotations

from pydantic import BaseModel


class MetricRequest(BaseModel):
    metric_name: str


class ApprovalRequest(BaseModel):
    metric_name: str
    reviewer: str = "Data Governance Lead"


class ConflictResolutionRequest(BaseModel):
    metric_name: str
    decision: str = "use certified definition"
