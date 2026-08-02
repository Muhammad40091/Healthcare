# Model Registry

Every promoted model version is tracked with:
- Version tag, training timestamp, holdout AUC
- Quality gate pass/fail per dimension (see quality-gates.md)
- Bias audit results (Fairness Monitor)
- Drift monitoring baseline (Drift Detector)
- Override log summary feeding the monthly calibration intelligence
  report described in the case study (Section 13)

See `src/denialiq_engine/risk_model/model_registry.py` for the reference
`ModelVersion` dataclass and promotion gate logic.
