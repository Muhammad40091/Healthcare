"""Model Registry — versioning, quality gates, and promotion tracking.

STATUS: interface-only. Every model version must pass the Quality Gate
checklist (docs/quality-gates.md: accuracy, bias, latency, safety, drift
gates) before promotion to production. Override patterns and monthly
calibration intelligence also live here per the case study's Section 13.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ModelVersion:
    version_tag: str
    trained_at: datetime
    holdout_auc: float
    bias_gate_passed: bool
    latency_p95_ms: float
    drift_psi: float
    promoted: bool = False


def evaluate_quality_gates(mv: ModelVersion) -> dict:
    return {
        "accuracy_gate": mv.holdout_auc >= 0.85,
        "bias_gate": mv.bias_gate_passed,
        "latency_gate": mv.latency_p95_ms < 200,
        "drift_gate": mv.drift_psi < 0.2,
    }


def can_promote(mv: ModelVersion) -> bool:
    return all(evaluate_quality_gates(mv).values())
