# AGENTS.md

You are building a production-style Data Engineering + Analytics Engineering + AI Governance project.

Project name:
Enterprise Metrics Trust Layer + Semantic Governance Platform

Primary goal:
Build a local semantic metrics platform that simulates how large enterprises govern business metrics, detect conflicting definitions, validate data contracts, track lineage, score trustworthiness, and expose certified metrics for dashboards and AI agents.

## Business Context

Large enterprises often suffer from metric inconsistency. Multiple teams define the same KPI differently. Dashboards disagree. Executives lose trust. AI assistants may retrieve or calculate the wrong metric.

This project must demonstrate that a data engineer can go beyond pipelines and build a trustworthy semantic data product layer.

## Core Outcome

The system should answer:

“Can this metric be trusted, explained, traced, versioned, and safely consumed?”

## Build Principles

- Write clean, modular, production-style Python.
- Use Python 3.12.
- Use type hints.
- Use docstrings for public functions.
- Use structured logging.
- Add error handling.
- Use synthetic data only.
- Do not use real sensitive data.
- Do not require external services in V0.1.
- Keep V0.1 deterministic and locally runnable.
- Simulate semantic layer concepts locally using YAML definitions and DuckDB.
- Every metric must have an owner, definition, formula, grain, dimensions, freshness rule, contract, and certification status.
- Every metric calculation must be reproducible.
- Every metric must include lineage.
- Every metric trust score must be explainable.
- Every major pipeline stage must have tests.
- README must be public-facing and recruiter-friendly.
- Technical docs must be strong enough for senior data engineers and analytics engineers.

## Definition of Done

- Code runs locally.
- Tests pass.
- Ruff passes.
- README is updated.
- Metric glossary exists.
- Semantic layer design doc exists.
- Metric contracts exist.
- Lineage outputs exist.
- Scorecards exist.
- Dashboard can run.
- API endpoints return valid JSON.
- GitHub Actions workflow exists.
- Docker files exist.
- STAR story is documented.
- LinkedIn post draft is included.
- No real sensitive data is used.
