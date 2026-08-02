# Quality Gate Architecture — Pre-Deployment Model Promotion

| Gate | Threshold | Action if failed |
|---|---|---|
| Accuracy Gate | Denial Prediction AUC >= 0.85 on holdout | Block promotion |
| Bias Gate | No demographic subgroup performance gap > 3% | Block and audit |
| Latency Gate | p95 inference latency < 200ms | Block and optimize |
| Safety Gate | No increase in false-negative rate on high-risk claims vs baseline | Mandatory human review |
| Drift Gate | Feature distribution PSI < 0.2 | Shadow-mode validation required |

See `src/denialiq_engine/risk_model/model_registry.py` for the
`ModelVersion` / `evaluate_quality_gates` implementation.
