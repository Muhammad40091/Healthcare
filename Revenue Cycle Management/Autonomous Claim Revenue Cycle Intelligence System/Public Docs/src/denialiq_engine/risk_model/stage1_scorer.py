"""Stage 1 — XGBoost fast-path denial risk scorer (production).

STATUS: prototype. Same architecture as the public demo
(denialiq-public/src/denialiq/risk_model), but trained on the client's
real de-identified historical claims (post PHI-tokenization) rather than
synthetic data, with the full production feature set (not just the 5
headline features) and versioned in the Model Registry.
"""
from __future__ import annotations

import pathlib

FEATURE_COLUMNS = [
    "cpt_payer_denial_rate",
    "missing_prior_auth",
    "icd10_specificity_score",
    "days_since_policy_update",
    "modifier_validity_score",
    # TODO(architect): extend with client-specific features discovered
    # during Phase 0 denial root-cause analysis (e.g. facility-level
    # patterns, coder-specific error rates, service-line risk factors).
]


class Stage1Scorer:
    def __init__(self, model_path: pathlib.Path, model_version: str):
        self.model_path = model_path
        self.model_version = model_version
        self.model = None  # TODO: load via joblib/mlflow model registry

    def load(self) -> None:
        raise NotImplementedError("Wire to Model Registry — see docs/model-registry.md")

    def score(self, features: dict) -> dict:
        raise NotImplementedError("Implement inference — see public demo for reference shape")
