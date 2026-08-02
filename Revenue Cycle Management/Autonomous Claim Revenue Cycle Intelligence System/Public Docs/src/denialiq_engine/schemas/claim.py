"""Production claim lifecycle schemas.

Superset of the public demo schemas: adds client-scoping, PHI-tokenized
patient reference, contract rate linkage, and audit metadata fields
required for real deployments. PHI is never stored directly — see
governance/phi_tokenizer.py.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, confloat


class PayerType(str, Enum):
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    COMMERCIAL = "commercial"
    SELF_PAY = "self_pay"


class ClaimStatus(str, Enum):
    BUILT = "built"
    CDI_REVIEWED = "cdi_reviewed"
    CODING_VALIDATED = "coding_validated"
    RISK_SCORED = "risk_scored"
    PENDING_PRIOR_AUTH = "pending_prior_auth"
    SUBMITTED = "submitted"
    PAID = "paid"
    DENIED = "denied"
    APPEALED = "appealed"
    APPEAL_OVERTURNED = "appeal_overturned"
    APPEAL_UPHELD = "appeal_upheld"
    WRITTEN_OFF = "written_off"


class Claim(BaseModel):
    claim_id: str
    client_id: str = Field(..., description="Hospital/client tenant identifier")
    patient_token: str = Field(..., description="PHI-tokenized patient reference, never a real MRN")
    payer_type: PayerType
    payer_name: str
    facility_id: str
    cpt_codes: list[str] = Field(default_factory=list)
    icd10_codes: list[str] = Field(default_factory=list)
    modifiers: list[str] = Field(default_factory=list)
    prior_auth_obtained: bool = False
    prior_auth_number: Optional[str] = None
    billed_amount: float = Field(..., ge=0)
    contracted_rate: Optional[float] = Field(
        default=None, description="Looked up from client_config contract rate table"
    )
    documentation_specificity_score: confloat(ge=0.0, le=1.0) = 0.5
    days_since_payer_policy_update: int = Field(default=0, ge=0)
    is_wiser_affected: bool = Field(
        default=False, description="True if claim falls under WISeR Model coverage criteria"
    )
    status: ClaimStatus = ClaimStatus.BUILT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RiskScore(BaseModel):
    claim_id: str
    stage1_score: confloat(ge=0.0, le=1.0)
    stage2_invoked: bool = False
    stage2_rationale: Optional[str] = None
    policy_citations: list[str] = Field(default_factory=list, description="RAG source doc IDs used in Stage 2")
    top_risk_features: list[str] = Field(default_factory=list)
    confidence: confloat(ge=0.0, le=1.0)
    model_version: str = Field(..., description="Model registry version tag for audit lineage")


class HITLTier(int, Enum):
    TIER_1_AUTO = 1
    TIER_2_BILLER = 2
    TIER_3_SENIOR_CODER = 3
    TIER_4_DIRECTOR = 4


class HITLDecision(BaseModel):
    claim_id: str
    tier: HITLTier
    sla_seconds: Optional[int] = None
    reason: str
    assigned_to: Optional[str] = None
    decided_at: Optional[datetime] = None
    override: bool = False
    override_rationale: Optional[str] = None


class AgentOutput(BaseModel):
    agent_name: str
    claim_id: str
    output: dict
    confidence: confloat(ge=0.0, le=1.0)
    rationale: str
    tool_calls: list[str] = Field(default_factory=list)
    model_version: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AppealDraft(BaseModel):
    claim_id: str
    denial_carc_codes: list[str]
    denial_rarc_codes: list[str] = Field(default_factory=list)
    root_cause_agent: Optional[str] = Field(
        default=None, description="Which agent's prior recommendation this denial traces back to"
    )
    policy_citations: list[str] = Field(default_factory=list)
    draft_text: str
    requires_human_approval: bool = True
    approved_by: Optional[str] = None
    filed_at: Optional[datetime] = None


class UnderpaymentAlert(BaseModel):
    claim_id: str
    payer_name: str
    contracted_rate: float
    paid_amount: float
    variance: float
    variance_type: str = Field(..., description="'isolated_error' or 'systematic_underpayment'")
    detected_at: datetime = Field(default_factory=datetime.utcnow)
