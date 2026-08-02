"""Drift Detector — weekly PSI monitoring on model input features.

STATUS: interface-only. Production version computes Population Stability
Index between the training distribution and a rolling window of live
scored claims, triggering the recalibration pipeline when PSI exceeds the
quality-gate threshold (0.2, see docs/quality-gates.md).
"""
from __future__ import annotations

import numpy as np


def population_stability_index(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """Standard PSI calculation between two 1D distributions."""
    breakpoints = np.quantile(expected, np.linspace(0, 1, bins + 1))
    breakpoints[0], breakpoints[-1] = -np.inf, np.inf

    expected_pct = np.histogram(expected, bins=breakpoints)[0] / len(expected)
    actual_pct = np.histogram(actual, bins=breakpoints)[0] / len(actual)

    expected_pct = np.clip(expected_pct, 1e-6, None)
    actual_pct = np.clip(actual_pct, 1e-6, None)

    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))


def check_drift(expected: np.ndarray, actual: np.ndarray, threshold: float = 0.2) -> dict:
    psi = population_stability_index(expected, actual)
    return {"psi": psi, "drifted": psi >= threshold, "threshold": threshold}
