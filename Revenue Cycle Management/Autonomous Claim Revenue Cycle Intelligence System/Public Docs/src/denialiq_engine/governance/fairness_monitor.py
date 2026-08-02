"""Fairness Monitor — bias audit on denial prediction outcomes.

STATUS: interface-only. Production version tracks denial flag rates across
service line, payer type, and demographic proxies (never direct protected
attributes — PHI-tokenized proxies only), alerting when any subgroup
diverges more than 2 standard deviations from the population mean.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def subgroup_disparity_report(df: pd.DataFrame, outcome_col: str, group_col: str) -> pd.DataFrame:
    """Return per-subgroup outcome rate and z-score vs population mean."""
    overall_mean = df[outcome_col].mean()
    overall_std = df[outcome_col].std()

    report = df.groupby(group_col)[outcome_col].agg(["mean", "count"]).reset_index()
    report["z_score"] = (report["mean"] - overall_mean) / (overall_std + 1e-9)
    report["flagged"] = report["z_score"].abs() > 2.0
    return report
