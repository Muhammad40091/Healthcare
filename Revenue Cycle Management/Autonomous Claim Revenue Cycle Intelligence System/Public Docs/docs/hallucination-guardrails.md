# Hallucination Guardrails — Trust by Design

- All LLM claim correction suggestions cross-validated by a deterministic
  rule engine before surfacing to billing users
- No LLM output displayed without a confidence score and rule-engine
  corroboration signal
- LLM-as-judge validation loop: a secondary LLM evaluates primary model
  suggestions for factual accuracy before human review
- SHAP feature importance values logged per decision — every flagged
  claim is explainable on demand
