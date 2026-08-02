"""Placeholder tests for governance modules. Expand as agents move from
interface-only to prototype/production status."""
from denialiq_engine.governance.hitl_router import route
from denialiq_engine.governance.drift_detector import population_stability_index
from denialiq_engine.schemas.claim import Claim, PayerType, RiskScore
import numpy as np


def test_hitl_router_tier1_auto():
    claim = Claim(
        claim_id="c1", client_id="demo", patient_token="tok123",
        payer_type=PayerType.MEDICARE, payer_name="Medicare", facility_id="f1",
        billed_amount=1200,
    )
    risk = RiskScore(claim_id="c1", stage1_score=0.02, confidence=0.97, model_version="v0-demo")
    decision = route(claim, risk)
    assert decision.tier.value == 1


def test_hitl_router_director_tier_on_high_value():
    claim = Claim(
        claim_id="c2", client_id="demo", patient_token="tok456",
        payer_type=PayerType.COMMERCIAL, payer_name="Aetna", facility_id="f1",
        billed_amount=30000,
    )
    risk = RiskScore(claim_id="c2", stage1_score=0.02, confidence=0.97, model_version="v0-demo")
    decision = route(claim, risk)
    assert decision.tier.value == 4


def test_psi_zero_for_identical_distributions():
    data = np.random.normal(0, 1, 1000)
    psi = population_stability_index(data, data)
    assert psi < 0.01
