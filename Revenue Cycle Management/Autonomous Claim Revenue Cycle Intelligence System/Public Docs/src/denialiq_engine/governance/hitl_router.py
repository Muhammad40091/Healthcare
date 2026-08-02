"""HITL Router — confidence-tiered human decision queue routing.

STATUS: prototype. Thresholds below match the case study's four-tier
matrix. Production deployments calibrate these per-client during Phase 0
(see client_config/) rather than using static values.
"""
from __future__ import annotations

from denialiq_engine.governance.audit_log import log_hitl_decision
from denialiq_engine.schemas.claim import Claim, HITLDecision, HITLTier, RiskScore

DEFAULT_THRESHOLDS = {
    "tier1_confidence_min": 0.95,
    "tier2_confidence_min": 0.80,
    "tier2_sla_seconds": 120,
    "tier3_sla_seconds": 900,
    "director_value_threshold": 25_000,
}


def route(claim: Claim, risk: RiskScore, thresholds: dict | None = None) -> HITLDecision:
    t = {**DEFAULT_THRESHOLDS, **(thresholds or {})}

    clean_claim_prob = 1 - risk.stage1_score

    if claim.billed_amount > t["director_value_threshold"]:
        decision = HITLDecision(
            claim_id=claim.claim_id,
            tier=HITLTier.TIER_4_DIRECTOR,
            sla_seconds=None,
            reason=f"Claim value ${claim.billed_amount:,.0f} exceeds director threshold",
        )
    elif risk.confidence >= t["tier1_confidence_min"] and clean_claim_prob >= t["tier1_confidence_min"]:
        decision = HITLDecision(
            claim_id=claim.claim_id,
            tier=HITLTier.TIER_1_AUTO,
            sla_seconds=None,
            reason="Confidence and clean-claim probability both >= 95%",
        )
    elif risk.confidence >= t["tier2_confidence_min"]:
        decision = HITLDecision(
            claim_id=claim.claim_id,
            tier=HITLTier.TIER_2_BILLER,
            sla_seconds=t["tier2_sla_seconds"],
            reason="Confidence 80-95%, biller review with SLA countdown",
        )
    else:
        decision = HITLDecision(
            claim_id=claim.claim_id,
            tier=HITLTier.TIER_3_SENIOR_CODER,
            sla_seconds=t["tier3_sla_seconds"],
            reason="Confidence below 80% or coding complexity flag",
        )

    log_hitl_decision(claim.claim_id, decision.tier.value, override=False, rationale=decision.reason)
    return decision
